from models.user import User
from extensions import db

def register_user(username, password):
    # 检查用户名是否存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {'error': '用户名已存在'}
    
    # 创建新用户
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return {'message': '用户注册成功'}

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None
