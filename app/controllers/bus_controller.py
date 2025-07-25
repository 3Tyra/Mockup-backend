from flask import request, jsonify
from app.services.bus_service import BusService
from app.utils.responses import success_response, error_response
from app.utils.middleware import token_required, roles_required

class BusController:
    @staticmethod
    @token_required
    @roles_required('driver')
    def register_bus(current_user):
        data = request.get_json()
        required_fields = ['registration_number', 'capacity', 'make', 'model']
        
        if not all(field in data for field in required_fields):
            return error_response('Missing required fields', 400)
        
        try:
            bus = BusService.register_bus(
                driver_id=current_user.id,
                registration_number=data['registration_number'],
                capacity=data['capacity'],
                make=data['make'],
                model=data['model']
            )
            return success_response('Bus registered successfully', bus.serialize(), 201)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response('Bus registration failed', 500)

    @staticmethod
    @token_required
    @roles_required('driver')
    def schedule_trip(current_user):
        data = request.get_json()
        required_fields = ['bus_id', 'route_id', 'departure_time', 'arrival_time', 'price_per_seat']
        
        if not all(field in data for field in required_fields):
            return error_response('Missing required fields', 400)
        
        try:
            schedule = BusService.schedule_trip(
                bus_id=data['bus_id'],
                route_id=data['route_id'],
                departure_time=data['departure_time'],
                arrival_time=data['arrival_time'],
                price_per_seat=data['price_per_seat'],
                driver_id=current_user.id
            )
            return success_response('Trip scheduled successfully', schedule.serialize(), 201)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response('Trip scheduling failed', 500)

    @staticmethod
    def get_available_buses():
        try:
            origin = request.args.get('origin')
            destination = request.args.get('destination')
            date = request.args.get('date')
            
            buses = BusService.get_available_buses(origin, destination, date)
            return success_response('Available buses retrieved', [bus.serialize() for bus in buses])
        except Exception as e:
            return error_response('Failed to retrieve available buses', 500)