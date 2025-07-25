from werkzeug.security import generate_password_hash
from app.models.user import User, UserRole
from app.utils.database import db
from datetime import datetime
import jwt
import os
from datetime import datetime, timedelta

class AuthService:
    @staticmethod
    def register_user(name, email, phone, password, role):
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            raise ValueError('Email already registered')
        
        # Create new user
        user = User(
            name=name,
            email=email,
            phone=phone,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            raise ValueError('Invalid email or password')
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'role': user.role.value,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, os.getenv('SECRET_KEY'), algorithm='HS256')
        
        return token