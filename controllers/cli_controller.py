from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.card import Card
# from models.comment import Comment
from datetime import date



db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Table created')

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            email = 'admin@spam.com',
            password = bcrypt.generate_password_hash('eggs').decode('utf-8'),
            is_admin = True,
        ),
        User(
            name = 'Tracey', 
            email = 'tracey@spam.com',
            password = bcrypt.generate_password_hash('12345').decode('utf-8'),
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    cards = [
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create the database',
            status = 'To Do',
            priority = 'High',
            date = date.today(),
            user = users[0]
        ),
        Card(
            title = "SQLAlchemy",
            description = "Stage 2 - Integrate ORM",
            status = "Ongoing",
            priority = "High",
            date = date.today(),
            user = users[0]
        ),
        Card(
            title = "ORM Queries",
            description = "Stage 3 - Implement several queries",
            status = "Ongoing",
            priority = "Medium",
            date = date.today(),
            user = users[1]
        ),
        Card(
            title = "Marshmallow",
            description = "Stage 4 - Implement Marshmallow to jsonify models",
            status = "Ongoing",
            priority = "Medium",
            date = date.today(),
            user = users[1]
        )
    ]

    db.session.add_all(cards)
    db.session.commit()
    
    # comments = [
    #     Comment(
    #         message= 'Nice one',
    #         user_id= 1,
    #         card_id= 1
    #     ),
    #     Comment(
    #         message= 'I love this',
    #         user_id= 2,
    #         card_id= 4
    #     ),
    #     Comment(
    #         message= 'Very important',
    #         user_id= 1,
    #         card_id= 3
    #     )
    # ]

    # db.session.add_all(comments)
    # db.session.commit()


    print('Tables seeded!')

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print('Tables dropped')