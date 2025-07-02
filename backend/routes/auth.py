from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import User
from extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')

    if not all([username, password, phone]):
        return jsonify({'error': '缺少必要字段'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400

    new_user = User(username=username, phone=phone)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '注册成功'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': '用户名或密码错误'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({
        'message': '登录成功',
        'access_token': access_token,
        'username': username
    }), 200

@auth_bp.route('/profile', methods=['GET'])
def profile():
    # 需要JWT验证
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    return jsonify({
        'username': user.username,
        'phone': user.phone,
        'created_at': user.created_at.isoformat()
    }), 200
