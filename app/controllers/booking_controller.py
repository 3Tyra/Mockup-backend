from flask import request, jsonify
from app.services.booking_service import BookingService
from app.utils.responses import success_response, error_response
from app.utils.middleware import token_required, roles_required

class BookingController:
    @staticmethod
    @token_required
    @roles_required('customer')
    def create_booking(current_user):
        data = request.get_json()
        required_fields = ['schedule_id', 'seat_number']
        
        if not all(field in data for field in required_fields):
            return error_response('Missing required fields', 400)
        
        try:
            booking = BookingService.create_booking(
                customer_id=current_user.id,
                schedule_id=data['schedule_id'],
                seat_number=data['seat_number']
            )
            return success_response('Booking created successfully', booking.serialize(), 201)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response('Booking creation failed', 500)

    @staticmethod
    @token_required
    @roles_required('customer')
    def get_user_bookings(current_user):
        try:
            bookings = BookingService.get_user_bookings(current_user.id)
            return success_response('Bookings retrieved', [booking.serialize() for booking in bookings])
        except Exception as e:
            return error_response('Failed to retrieve bookings', 500)

    @staticmethod
    @token_required
    @roles_required('customer')
    def cancel_booking(current_user, booking_id):
        try:
            booking = BookingService.cancel_booking(booking_id, current_user.id)
            return success_response('Booking cancelled successfully', booking.serialize())
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response('Booking cancellation failed', 500)