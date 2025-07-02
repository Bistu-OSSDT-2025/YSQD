from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Reservation, User, Venue
from ..extensions import db
from datetime import datetime

reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('/', methods=['POST'])
@jwt_required()
def create_reservation():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    data = request.get_json()
    venue_id = data.get('venue_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not all([venue_id, start_time, end_time]):
        return jsonify({'error': '缺少必要字段'}), 400

    try:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
    except ValueError:
        return jsonify({'error': '时间格式不正确'}), 400

    # 检查场馆是否存在
    venue = Venue.query.get(venue_id)
    if not venue:
        return jsonify({'error': '场馆不存在'}), 404

    # 检查时间冲突
    conflicting = Reservation.query.filter(
        Reservation.venue_id == venue_id,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time,
        Reservation.status == 'confirmed'
    ).first()

    if conflicting:
        return jsonify({'error': '该时间段已被预约'}), 400

    # 创建预约
    reservation = Reservation(
        user_id=user.id,
        venue_id=venue_id,
        start_time=start_time,
        end_time=end_time,
        status='pending'
    )
    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        'message': '预约申请已提交',
        'reservation_id': reservation.id
    }), 201

@reservations_bp.route('/', methods=['GET'])
@jwt_required()
def get_reservations():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    reservations = Reservation.query.filter_by(user_id=user.id).all()
    return jsonify([{
        'id': r.id,
        'venue_id': r.venue_id,
        'venue_name': r.venue.name,
        'start_time': r.start_time.isoformat(),
        'end_time': r.end_time.isoformat(),
        'status': r.status,
        'created_at': r.created_at.isoformat()
    } for r in reservations]), 200

@reservations_bp.route('/<int:reservation_id>', methods=['DELETE'])
@jwt_required()
def cancel_reservation(reservation_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': '预约不存在'}), 404

    if reservation.user_id != user.id:
        return jsonify({'error': '无权操作此预约'}), 403

    if reservation.status == 'cancelled':
        return jsonify({'error': '预约已取消'}), 400

    reservation.status = 'cancelled'
    db.session.commit()

    return jsonify({'message': '预约已取消'}), 200
