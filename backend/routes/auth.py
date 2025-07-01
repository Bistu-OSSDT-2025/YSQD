from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.auth_service import register_user, authenticate_user
from utils.validators import validate_username, validate_password

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 验证输入
    if not validate_username(username):
        return jsonify({'error': '用户名格式无效（3-20个字符）'}), 400
    if not validate_password(password):
        return jsonify({'error': '密码格式无效（至少6个字符）'}), 400
    
    # 注册用户
    result = register_user(username, password)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify({'message': '用户注册成功'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate_user(username, password)
    if not user:
        return jsonify({'error': '用户名或密码错误'}), 401
    
    # 生成JWT令牌
    access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
    return jsonify(access_token=access_token), 200
