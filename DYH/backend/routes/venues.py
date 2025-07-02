from flask import Blueprint, jsonify
from ..models import Venue
from ..extensions import db

venues_bp = Blueprint('venues', __name__)

@venues_bp.route('/', methods=['GET'])
def get_venues():
    venues = Venue.query.all()
    return jsonify([{
        'id': venue.id,
        'name': venue.name,
        'type': venue.type,
        'description': venue.description,
        'image_url': venue.image_url,
        'capacity': venue.capacity
    } for venue in venues]), 200

@venues_bp.route('/<int:venue_id>', methods=['GET'])
def get_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return jsonify({'error': '场馆不存在'}), 404
    
    return jsonify({
        'id': venue.id,
        'name': venue.name,
        'type': venue.type,
        'description': venue.description,
        'image_url': venue.image_url,
        'capacity': venue.capacity,
        'available_slots': get_available_slots(venue_id)  # 需要实现这个函数
    }), 200

def get_available_slots(venue_id):
    # TODO: 实现获取可用时间段的逻辑
    return []
