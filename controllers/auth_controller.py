from flask import Blueprint, request, abort
from init import db, bcrypt
from models.user import User, UserSchema
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

@auth_bp.route('/register/', methods=['POST'])
@jwt_required()
def auth_register():
    try:
        user = User(
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
            name = request.json.get('name')
        )
        db.session.add(user)
        db.session.commit()
        #Respond to the user
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409

@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    stmt = db.select(User).filter_by(email = request.json["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, request.json["password"]):
        # return UserSchema(exclude=["password"]).dump(user), 200
        # generate token
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {"error": "Invalid email or password"}, 401 #401 Unauthorized


def authorize():
    user_id = get_jwt_identity() #extract the user identity from the token
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    print(user_id)
    if not user.is_admin:
        abort(401)
