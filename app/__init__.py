from flask import Flask                 # Core Flask web framework
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy = ORM (database handler)
from flask_login import LoginManager    # Flask-Login = user session management
from config import Config               # Pull our app settings from config.py

# Create global instances (they'll be attached to the app in create_app)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'  # Where to redirect if @login_required fails

# Factory function to build our app and register parts
def create_app():
    app = Flask(__name__)                  # Create the Flask app object
    app.config.from_object(Config)         # Load settings from Config class

    db.init_app(app)                       # Bind database to this app
    login_manager.init_app(app)           # Enable login manager (auth handling)

    # Import routes and models (routes = page logic, models = DB structure)
    from app import routes, models

    # Register Blueprint for routes (keeps app modular and clean)
    app.register_blueprint(routes.bp)

    return app