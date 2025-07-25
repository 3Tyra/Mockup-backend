from flask import request, jsonify
from app.models.user import User, UserRole
from app.services.auth_service import AuthService
from app.utils.responses import success_response, error_response
from app.utils.middleware import token_required, roles_required

class AuthController:
    @staticmethod
    def register():
        data = request.get_json()
        required_fields = ['name', 'email', 'phone', 'password', 'role']
        
        if not all(field in data for field in required_fields):
            return error_response('Missing required fields', 400)
        
        try:
            user = AuthService.register_user(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                password=data['password'],
                role=UserRole(data['role'])
            )
            return success_response('User registered successfully', user.serialize(), 201)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response('Registration failed', 500)

    @staticmethod
    def login():
        data = request.get_json()
        required_fields = ['email', 'password']
        
        if not all(field in data for field in required_fields):
            return error_response('Missing required fields', 400)
        
        try:
            token = AuthService.login_user(data['email'], data['password'])
            return success_response('Login successful', {'token': token})
        except ValueError as e:
            return error_response(str(e), 401)
        except Exception as e:
            return error_response('Login failed', 500)

    @staticmethod
    @token_required
    def get_profile(current_user):
        return success_response('Profile retrieved', current_user.serialize())