from flask import request, jsonify
from app.services.admin_service import AdminService
from app.utils.responses import success_response, error_response
from app.utils.middleware import token_required, roles_required

class AdminController:
    @staticmethod
    @token_required
    @roles_required('admin')
    def get_all_users(current_user):
        try:
            users = AdminService.get_all_users()
            return success_response('Users retrieved', [user.serialize() for user in users])
        except Exception as e:
            return error_response('Failed to retrieve users', 500)

    @staticmethod
    @token_required
    @roles_required('admin')
    def create_route(current_user):
        data = request.get_json()
        required_fields = ['origin', 'destination', 'distance', 'estimated_duration']
        
        if not all(field in data for field in required_fields):
            return error_response('Missing required fields', 400)
        
        try:
            route = AdminService.create_route(
                origin=data['origin'],
                destination=data['destination'],
                distance=data['distance'],
                estimated_duration=data['estimated_duration']
            )
            return success_response('Route created successfully', route.serialize(), 201)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response('Route creation failed', 500)

    @staticmethod
    @token_required
    @roles_required('admin')
    def get_dashboard_stats(current_user):
        try:
            stats = AdminService.get_dashboard_stats()
            return success_response('Dashboard stats retrieved', stats)
        except Exception as e:
            return error_response('Failed to retrieve dashboard stats', 500)