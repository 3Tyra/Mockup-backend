from app.models.booking import Booking
from app.models.route import BusSchedule
from app.utils.database import db

class BookingService:
    @staticmethod
    def create_booking(customer_id, schedule_id, seat_number):
        # Check if schedule exists
        schedule = BusSchedule.query.get(schedule_id)
        if not schedule:
            raise ValueError('Schedule not found')
        
        # Check if seat is available
        existing_booking = Booking.query.filter_by(
            schedule_id=schedule_id,
            seat_number=seat_number,
            status='confirmed'
        ).first()
        
        if existing_booking:
            raise ValueError('Seat already booked')
        
        # Check if seat number is valid
        bus = schedule.bus
        if seat_number < 1 or seat_number > bus.capacity:
            raise ValueError('Invalid seat number')
        
        # Create new booking
        booking = Booking(
            customer_id=customer_id,
            schedule_id=schedule_id,
            seat_number=seat_number,
            fare=schedule.price_per_seat
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return booking

    @staticmethod
    def get_user_bookings(user_id):
        return Booking.query.filter_by(customer_id=user_id).all()

    @staticmethod
    def cancel_booking(booking_id, user_id):
        booking = Booking.query.filter_by(id=booking_id, customer_id=user_id).first()
        
        if not booking:
            raise ValueError('Booking not found')
        
        if booking.status == 'cancelled':
            raise ValueError('Booking already cancelled')
        
        booking.status = 'cancelled'
        db.session.commit()
        
        return booking