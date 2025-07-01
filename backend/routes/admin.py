from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.booking_service import get_all_bookings, update_booking_status
from models.user import User

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/bookings', methods=['GET'])
@jwt_required()
def manage_bookings():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # 验证管理员权限
    if not user or not user.is_admin():
        return jsonify({'error': '仅管理员可访问'}), 403
    
    status = request.args.get('status', 'pending')
    bookings = get_all_bookings(status)
    return jsonify([booking.serialize() for booking in bookings]), 200

@bp.route('/bookings/<int:booking_id>', methods=['PUT'])
@jwt_required()
def review_booking(booking_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': '仅管理员可操作'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['confirmed', 'cancelled']:
        return jsonify({'error': '无效的状态更新'}), 400
    
    result = update_booking_status(booking_id, new_status)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify({'message': '预约状态已更新'}), 200
