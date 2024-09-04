"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app            # Assign app to db.app context
    db.init_app(app)        # Pass app to init_app function

class User(db.Model):

    """User Model/Class that has firstname, lastname, and image profile url. Referenced by the Post Model/Class"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,                  # Our PK
                   primary_key = True,
                   autoincrement = True)
    firstname = db.Column(db.String(40),        # Both names should be not null
                          nullable = False)
    lastname = db.Column(db.String(40),
                         nullable = False)
    image_url = db.Column(db.String,
                          nullable = False)     # Want all users to have some sort of image.
    
    posts = db.relationship("Post", cascade = 'all, delete-orphan')


class Post(db.Model):

    """Post Model/Class that has title, content, creation date and has foreign key to User.id"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                  primary_key = True,
                  autoincrement = True)
    
    title = db.Column(db.String(40),
                  nullable = False)
    
    content = db.Column(db.String(40),
                  nullable = False)
    
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete = 'cascade'))

    users = db.relationship("User")
    