from flask import Blueprint, request
from init import db
from models.user import User, UserSchema
from controllers.auth_controller import authorize
from datetime import date
from flask_jwt_extended import jwt_required

users_bp = Blueprint('users', __name__, url_prefix = '/users')

@users_bp.route('/')
def get_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True).dump(users)

@users_bp.route('/<int:user_id>')
def get_user(user_id):
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    return UserSchema().dump(user)

