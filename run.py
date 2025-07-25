from flask import Flask
from app.controllers.auth_controller import AuthController
from app.controllers.bus_controller import BusController
from app.controllers.booking_controller import BookingController
from app.controllers.admin_controller import AdminController
from app.utils.database import init_db
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Auth routes
    app.add_url_rule('/api/auth/register', view_func=AuthController.register, methods=['POST'])
    app.add_url_rule('/api/auth/login', view_func=AuthController.login, methods=['POST'])
    app.add_url_rule('/api/auth/profile', view_func=AuthController.get_profile, methods=['GET'])
    
    # Bus routes
    app.add_url_rule('/api/buses', view_func=BusController.register_bus, methods=['POST'])
    app.add_url_rule('/api/buses/schedule', view_func=BusController.schedule_trip, methods=['POST'])
    app.add_url_rule('/api/buses/available', view_func=BusController.get_available_buses, methods=['GET'])
    
    # Booking routes
    app.add_url_rule('/api/bookings', view_func=BookingController.create_booking, methods=['POST'])
    app.add_url_rule('/api/bookings', view_func=BookingController.get_user_bookings, methods=['GET'])
    app.add_url_rule('/api/bookings/<int:booking_id>/cancel', view_func=BookingController.cancel_booking, methods=['PUT'])
    
    # Admin routes
    app.add_url_rule('/api/admin/users', view_func=AdminController.get_all_users, methods=['GET'])
    app.add_url_rule('/api/admin/routes', view_func=AdminController.create_route, methods=['POST'])
    app.add_url_rule('/api/admin/stats', view_func=AdminController.get_dashboard_stats, methods=['GET'])
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)