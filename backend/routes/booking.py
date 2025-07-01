from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.booking_service import create_booking, get_user_bookings, cancel_booking
from utils.validators import validate_booking_data
from utils.time_utils import parse_datetime

bp = Blueprint('booking', __name__, url_prefix='/bookings')

@bp.route('/', methods=['POST'])
@jwt_required()
def book_venue():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # 验证预约数据
    errors = validate_booking_data(data)
    if errors:
        return jsonify(errors), 400
    
    # 转换时间格式
    try:
        start_time = parse_datetime(data['start_time'])
        end_time = parse_datetime(data['end_time'])
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    # 创建预约
    booking = create_booking(user_id, data['venue_id'], start_time, end_time)
    if booking.get('error'):
        return jsonify(booking), 400
    return jsonify(booking.serialize()), 201

@bp.route('/user', methods=['GET'])
@jwt_required()
def user_bookings():
    user_id = get_jwt_identity()
    bookings = get_user_bookings(user_id)
    return jsonify([booking.serialize() for booking in bookings]), 200

@bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    user_id = get_jwt_identity()
    result = cancel_booking(user_id, booking_id)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify({'message': '预约已取消'}), 200
