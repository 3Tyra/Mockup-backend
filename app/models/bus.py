from datetime import datetime
from app.utils.database import db

class Bus(db.Model):
    __tablename__ = 'buses'
    
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    schedules = db.relationship('BusSchedule', backref='bus', lazy=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'registration_number': self.registration_number,
            'capacity': self.capacity,
            'make': self.make,
            'model': self.model,
            'driver_id': self.driver_id,
            'created_at': self.created_at.isoformat()
        }