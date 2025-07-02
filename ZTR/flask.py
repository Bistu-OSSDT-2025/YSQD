from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 创建 Flask 应用实例
app = Flask(__name__)
# 配置数据库，这里用 SQLite 演示，可按需换 MySQL 等
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///venue_reservation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 初始化 SQLAlchemy，用于操作数据库
db = SQLAlchemy(app)

# 设计数据库表结构（以场馆预约时段 Slots 表为例）
class Slots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    booked_by = db.Column(db.String(100), nullable=True)

# 实现核心预约逻辑 - 预约冲突检测
def check_availability(slot_id):
    slot = db.session.execute(
        db.select(Slots).filter_by(id=slot_id)
    ).scalar_one_or_none()
    return slot.booked_by is None if slot else False

# （可选）简单路由，用于测试框架和逻辑，可根据实际需求扩展接口
@app.route('/')
def hello_world():
    return 'Flask 应用框架已搭建，可扩展更多功能！'

if __name__ == '__main__':
    # 创建数据库表（首次运行时，确保在应用上下文里）
    with app.app_context():
        db.create_all()
    app.run(debug=True)