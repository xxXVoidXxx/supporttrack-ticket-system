from datetime import datetime
from app import db  # Our SQLAlchemy instance from __init__.py
from flask_login import UserMixin  # Gives User session/login powers
from app import login_manager      # Needed to load users into session

# User model = one row per registered user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing ID
    email = db.Column(db.String(120), unique=True, nullable=False)  # Login ID
    password = db.Column(db.String(128), nullable=False)            # Hashed pw
    is_admin = db.Column(db.Boolean, default=False)                 # Role flag

    # One user can have many tickets (a one-to-many relationship).
    tickets = db.relationship('Ticket', backref='author', lazy=True)

# Ticket model = one row per submitted help ticket
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Ticket ID
    title = db.Column(db.String(120), nullable=False)  # Short title
    description = db.Column(db.Text, nullable=False)   # Full issue text
    status = db.Column(db.String(20), default='Open')  # Open/In Progress/Closed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Submission time

    # Foreign key: ties this ticket to the submitting user's ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# This function tells Flask-Login how to retrieve a user object from a session ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Looks up user in DB by primary key
