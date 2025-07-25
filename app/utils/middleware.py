from functools import wraps
from flask import request, jsonify
import jwt
import os
from app.models.user import UserRole
from app.utils.responses import error_response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return error_response('Token is missing', 401)
        
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            current_user = {
                'id': data['user_id'],
                'role': UserRole(data['role'])
            }
        except:
            return error_response('Token is invalid', 401)
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user['role'].value not in roles:
                return error_response('Unauthorized access', 403)
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator