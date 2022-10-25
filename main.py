from flask import Flask 
from controllers.cards_controller import cards_bp
from controllers.auth_controller import auth_bp
from init import db, ma, bcrypt, jwt

import os

def create_app(): #automatically called if it is named create_app(). otherwise, need to specify in the .flaskenv
    app = Flask(__name__)

    @app.errorhandler(404)
    def not_found(err):
        return {'Error': str(err)}, 404

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JSON_SORT_KEYS'] = False
    
    ma.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(cards_bp)
    app.register_blueprint(auth_bp)

    return app
