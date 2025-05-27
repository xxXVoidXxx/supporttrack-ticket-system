import os  # For checking environment variables (can override settings in prod)

# Define settings in a class for reusability
class Config:
    # Secret key is used to sign session cookies, CSRF tokens, etc.
    # Secret key protects sessions and forms from tampering
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLAlchemy will use a local SQLite file to store your data
    SQLALCHEMY_DATABASE_URI = 'sqlite:///supporttrack.db'

    # This suppresses warning messages we don’t need right now
    SQLALCHEMY_TRACK_MODIFICATIONS = False