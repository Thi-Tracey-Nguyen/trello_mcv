from flask import Flask 
from controllers.cards_controller import cards_bp
from db import db, ma

import os

def create_app(): #automatically called if it is named create_app(). otherwise, need to specify in the .flaskenv
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS'] = False
    
    ma.init_app(app)
    db.init_app(app)

    app.register_blueprint(cards_bp)

    return app
