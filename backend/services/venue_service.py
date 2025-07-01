from models.venue import Venue
from extensions import db

def get_all_venues():
    return Venue.query.all()

def create_venue(data):
    venue = Venue(
        name=data['name'],
        capacity=data['capacity'],
        description=data.get('description', '')
    )
    db.session.add(venue)
    db.session.commit()
    return venue

def update_venue(venue_id, data):
    venue = Venue.query.get(venue_id)
    if not venue:
        return None
    
    venue.name = data['name']
    venue.capacity = data['capacity']
    venue.description = data.get('description', venue.description)
    db.session.commit()
    return venue

def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return False
    
    db.session.delete(venue)
    db.session.commit()
    return True
