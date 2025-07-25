from app.models.user import User
from app.models.route import Route
from app.models.bus import Bus
from app.models.booking import Booking
from app.utils.database import db

class AdminService:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def create_route(origin, destination, distance, estimated_duration):
        # Check if route already exists
        existing_route = Route.query.filter_by(
            origin=origin,
            destination=destination
        ).first()
        
        if existing_route:
            raise ValueError('Route already exists')
        
        # Create new route
        route = Route(
            origin=origin,
            destination=destination,
            distance=distance,
            estimated_duration=estimated_duration
        )
        
        db.session.add(route)
        db.session.commit()
        
        return route

    @staticmethod
    def get_dashboard_stats():
        stats = {
            'total_users': User.query.count(),
            'total_drivers': User.query.filter_by(role='driver').count(),
            'total_customers': User.query.filter_by(role='customer').count(),
            'total_buses': Bus.query.count(),
            'total_bookings': Booking.query.count(),
            'active_routes': Route.query.count()
        }
        
        return stats