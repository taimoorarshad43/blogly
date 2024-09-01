"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app            # Assign app to db.app context
    db.init_app(app)        # Pass app to init_app function

class Users(db.Model):
    id = db.Column(db.Integer,                  # Our PK
                   primary_key = True,
                   autoincrement = True)
    firstname = db.Column(db.String(40),        # Both names should be not null
                          nullable = False)
    lastname = db.Column(db.String(40),
                         nullable = False)
    image_url = db.Column(db.String)            # What if the user is shy?


    