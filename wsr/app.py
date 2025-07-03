from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    bookings = db.relationship('Booking', backref='facility', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 初始化数据库
@app.before_first_request
def create_tables():
    db.create_all()
    # 如果数据库为空，添加默认场馆
    if Facility.query.count() == 0:
        facilities = [
            {'name': '羽毛球馆 A', 'type': 'badminton', 'price_per_hour': 35},
            {'name': '健身房 B', 'type': 'gym', 'price_per_hour': 45},
            {'name': '乒乓球馆 C', 'type': 'table_tennis', 'price_per_hour': 25}
        ]
        for facility in facilities:
            db.session.add(Facility(**facility))
        db.session.commit()

# 路由
@app.route('/')
def index():
    return render_template('index.html')

# API路由
@app.route('/api/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': '未登录'
        })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        session['user_id'] = user.id
        return jsonify({
            'success': True,
            'message': '登录成功'
        })
    else:
        return jsonify({
            'success': False,
            'message': '用户名或密码错误'
        })

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({
        'success': True,
        'message': '已登出'
    })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    # 检查用户名或邮箱是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({
            'success': False,
            'message': '用户名已存在'
        })
    
    if User.query.filter_by(email=email).first():
        return jsonify({
            'success': False,
            'message': '邮箱已存在'
        })
    
    # 创建新用户
    new_user = User(
        username=username,
        name=name,
        email=email,
        password=password  # 注意：在实际应用中应加密存储密码
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '注册成功'
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    facilities_count = Facility.query.count()
    bookings_count = Booking.query.count()
    users_count = User.query.count()
    
    return jsonify({
        'facilities': facilities_count,
        'bookings': bookings_count,
        'users': users_count,
        'rating': 4.9  # 固定评分
    })

@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    facilities = Facility.query.all()
    result = []
    
    for facility in facilities:
        result.append({
            'id': facility.id,
            'name': facility.name,
            'type': facility.type,
            'price_per_hour': facility.price_per_hour
        })
    
    return jsonify(result)

@app.route('/api/bookings/available', methods=['GET'])
def get_available_time_slots():
    facility_id = request.args.get('facility_id')
    date = request.args.get('date')
    
    if not facility_id or not date:
        return jsonify([])
    
    # 生成从8:00到22:00的时间段
    time_slots = []
    for hour in range(8, 22):
        # 检查该时间段是否已被预约
        booking = Booking.query.filter_by(
            facility_id=facility_id,
            date=date,
            hour=hour,
            status='confirmed'
        ).first()
        
        time_slots.append({
            'hour': hour,
            'start_time': f'{hour}:00',
            'end_time': f'{hour+1}:00',
            'is_available': booking is None
        })
    
    return jsonify(time_slots)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': '请先登录'
        }), 401
    
    data = request.get_json()
    facility_id = data.get('facility_id')
    date = data.get('date')
    hour = data.get('hour')
    
    # 检查该时间段是否已被预约
    booking_exists = Booking.query.filter_by(
        facility_id=facility_id,
        date=date,
        hour=hour,
        status='confirmed'
    ).first()
    
    if booking_exists:
        return jsonify({
            'success': False,
            'message': '该时间段已被预约'
        })
    
    # 创建新预约
    new_booking = Booking(
        user_id=session['user_id'],
        facility_id=facility_id,
        date=date,
        hour=hour
    )
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '预约成功',
        'booking': {
            'id': new_booking.id,
            'user_id': new_booking.user_id,
            'facility_id': new_booking.facility_id,
            'date': new_booking.date,
            'hour': new_booking.hour,
            'status': new_booking.status,
            'created_at': new_booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    })

@app.route('/api/bookings', methods=['GET'])
def get_my_bookings():
    if 'user_id' not in session:
        return jsonify([])
    
    bookings = Booking.query.filter_by(
        user_id=session['user_id']
    ).join(Facility).all()
    
    result = []
    for booking in bookings:
        result.append({
            'id': booking.id,
            'facility_id': booking.facility_id,
            'facility_name': booking.facility.name,
            'date': booking.date,
            'hour': booking.hour,
            'start_time': f'{booking.hour}:00',
            'end_time': f'{booking.hour+1}:00',
            'status': booking.status,
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(result)

@app.route('/api/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': '请先登录'
        }), 401
    
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({
            'success': False,
            'message': '预约不存在'
        }), 404
    
    if booking.user_id != session['user_id']:
        return jsonify({
            'success': False,
            'message': '无权修改此预约'
        }), 403
    
    data = request.get_json()
    status = data.get('status')
    
    if status:
        booking.status = status
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '预约状态已更新'
        })
    else:
        return jsonify({
            'success': False,
            'message': '未提供有效状态'
        }), 400

if __name__ == '__main__':
    app.run(debug=True)    