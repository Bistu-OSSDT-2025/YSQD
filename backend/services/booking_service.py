from models.booking import Booking
from models.venue import Venue
from extensions import db
from datetime import datetime
from sqlalchemy import and_

def create_booking(user_id, venue_id, start_time, end_time):
    # 检查场馆是否存在
    venue = Venue.query.get(venue_id)
    if not venue:
        return {'error': '场馆不存在'}
    
    # 检查时间冲突
    conflict = Booking.query.filter(
        Booking.venue_id == venue_id,
        Booking.end_time > start_time,
        Booking.start_time < end_time,
        Booking.status != 'cancelled'
    ).first()
    
    if conflict:
        return {'error': '该时段已被预约'}
    
    # 创建预约
    booking = Booking(
        user_id=user_id,
        venue_id=venue_id,
        start_time=start_time,
        end_time=end_time,
        status='pending'
    )
    db.session.add(booking)
    db.session.commit()
    return booking

def get_user_bookings(user_id):
    return Booking.query.filter_by(user_id=user_id).all()

def get_all_bookings(status=None):
    query = Booking.query
    if status:
        query = query.filter_by(status=status)
    return query.all()

def cancel_booking(user_id, booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return {'error': '预约不存在'}
    
    if booking.user_id != user_id:
        return {'error': '无权取消此预约'}
    
    if booking.status == 'cancelled':
        return {'error': '预约已取消'}
    
    booking.status = 'cancelled'
    db.session.commit()
    return {'message': '预约取消成功'}

def update_booking_status(booking_id, status):
    booking = Booking.query.get(booking_id)
    if not booking:
        return {'error': '预约不存在'}
    
    if booking.status == 'cancelled':
        return {'error': '无法更新已取消的预约'}
    
    booking.status = status
    db.session.commit()
    return {'message': '状态更新成功'}
