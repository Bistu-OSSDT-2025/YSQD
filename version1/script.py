from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import uuid
import bcrypt

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据模型
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Venue(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(40), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    status = db.Column(db.String(20), default="可预约")
    bookings = db.relationship('Booking', backref='venue', lazy=True)

class Booking(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    venue_id = db.Column(db.String(36), db.ForeignKey('venue.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default="已确认")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 工具函数
def generate_booking_number():
    return f"BOOK{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:5].upper()}"

# API路由
@app.route('/api/venues', methods=['GET'])
def get_venues():
    venues = Venue.query.all()
    result = []
    for venue in venues:
        venue_data = {
            'id': venue.id,
            'name': venue.name,
            'type': venue.type,
            'location': venue.location,
            'capacity': venue.capacity,
            'price_per_hour': venue.price_per_hour,
            'description': venue.description,
            'image_url': venue.image_url,
            'status': venue.status
        }
        result.append(venue_data)
    return jsonify(result)

@app.route('/api/venues/<venue_id>', methods=['GET'])
def get_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    return jsonify({
        'id': venue.id,
        'name': venue.name,
        'type': venue.type,
        'location': venue.location,
        'capacity': venue.capacity,
        'price_per_hour': venue.price_per_hour,
        'description': venue.description,
        'image_url': venue.image_url,
        'status': venue.status
    })

@app.route('/api/bookings', methods=['GET'])
def get_user_bookings():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    bookings = Booking.query.filter_by(user_id=user_id).all()
    result = []
    for booking in bookings:
        venue = Venue.query.get(booking.venue_id)
        booking_data = {
            'id': booking.id,
            'booking_number': booking.booking_number,
            'venue': {
                'id': venue.id,
                'name': venue.name,
                'image_url': venue.image_url,
                'type': venue.type
            },
            'date': booking.date.strftime('%Y-%m-%d'),
            'start_time': booking.start_time,
            'end_time': booking.end_time,
            'status': booking.status,
            'price': venue.price_per_hour * (int(booking.end_time.split(':')[0]) - int(booking.start_time.split(':')[0]))
        }
        result.append(booking_data)
    return jsonify(result)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    required_fields = ['user_id', 'venue_id', 'date', 'start_time', 'end_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # 检查时间段是否已被预约
    existing_booking = Booking.query.filter_by(
        venue_id=data['venue_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        start_time=data['start_time']
    ).first()
    
    if existing_booking:
        return jsonify({'error': 'This time slot is already booked'}), 400
    
    booking = Booking(
        booking_number=generate_booking_number(),
        user_id=data['user_id'],
        venue_id=data['venue_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        start_time=data['start_time'],
        end_time=data['end_time']
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({
        'message': 'Booking created successfully',
        'booking_id': booking.id,
        'booking_number': booking.booking_number
    }), 201

@app.route('/api/bookings/<booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.status == '已完成' or booking.status == '已取消':
        return jsonify({'error': 'Cannot cancel a completed or already cancelled booking'}), 400
    
    booking.status = '已取消'
    db.session.commit()
    
    return jsonify({'message': 'Booking cancelled successfully'})

@app.route('/api/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user.id,
        'username': user.username
    }), 201

@app.route('/api/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    return jsonify({
        'message': 'Login successful',
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)    