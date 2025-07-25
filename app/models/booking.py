from datetime import datetime
from app.utils.database import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('bus_schedules.id'), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    fare = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'schedule_id': self.schedule_id,
            'seat_number': self.seat_number,
            'fare': self.fare,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }