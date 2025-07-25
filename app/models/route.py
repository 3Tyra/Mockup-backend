from datetime import datetime
from app.utils.database import db

class Route(db.Model):
    __tablename__ = 'routes'
    
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    estimated_duration = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    schedules = db.relationship('BusSchedule', backref='route', lazy=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'origin': self.origin,
            'destination': self.destination,
            'distance': self.distance,
            'estimated_duration': self.estimated_duration,
            'created_at': self.created_at.isoformat()
        }

class BusSchedule(db.Model):
    __tablename__ = 'bus_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    price_per_seat = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='schedule', lazy=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'bus_id': self.bus_id,
            'route_id': self.route_id,
            'departure_time': self.departure_time.isoformat(),
            'arrival_time': self.arrival_time.isoformat(),
            'price_per_seat': self.price_per_seat,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }