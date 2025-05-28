# Import the create_app function and the database object (db)
# One-time script to initialize the database schema on Render (or any other production deployment)
from app import create_app, db

# Create a Flask app instance using the factory pattern
app = create_app()

# Use the app's context so SQLAlchemy can bind models to the correct app
with app.app_context():
    # Create all database tables based on models defined in models.py
    db.create_all()

    # Confirm it worked
    print("✅ Database initialized successfully!")