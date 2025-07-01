from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.venue_service import get_all_venues, create_venue, update_venue, delete_venue
from utils.validators import validate_venue_data

bp = Blueprint('venue', __name__, url_prefix='/venues')

@bp.route('/', methods=['GET'])
def list_venues():
    venues = get_all_venues()
    return jsonify([venue.serialize() for venue in venues]), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def add_venue():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # 验证管理员权限
    if not current_user_id.is_admin():
        return jsonify({'error': '仅管理员可添加场馆'}), 403
    
    # 验证数据
    errors = validate_venue_data(data)
    if errors:
        return jsonify(errors), 400
    
    venue = create_venue(data)
    return jsonify(venue.serialize()), 201

@bp.route('/<int:venue_id>', methods=['PUT'])
@jwt_required()
def modify_venue(venue_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not current_user_id.is_admin():
        return jsonify({'error': '仅管理员可修改场馆'}), 403
    
    errors = validate_venue_data(data)
    if errors:
        return jsonify(errors), 400
    
    venue = update_venue(venue_id, data)
    if not venue:
        return jsonify({'error': '场馆不存在'}), 404
    return jsonify(venue.serialize()), 200

@bp.route('/<int:venue_id>', methods=['DELETE'])
@jwt_required()
def remove_venue(venue_id):
    current_user_id = get_jwt_identity()
    
    if not current_user_id.is_admin():
        return jsonify({'error': '仅管理员可删除场馆'}), 403
    
    if delete_venue(venue_id):
        return jsonify({'message': '场馆已删除'}), 200
    return jsonify({'error': '场馆不存在'}), 404
