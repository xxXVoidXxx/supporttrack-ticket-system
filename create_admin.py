# create_admin.py
# Safe and structured script to add an admin user to the database

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    """Logic to create an admin user in the database."""
    admin_email = 'admin@example.com'
    admin_password = 'YourSecurePassword123!'  # Be sure to change this later

    # Check for existing user to avoid duplicates
    existing_user = User.query.filter_by(email=admin_email).first()
    if existing_user:
        print(f"⚠️ User with email '{admin_email}' already exists.")
        return

    # Create new admin user with hashed password
    admin_user = User(
        email=admin_email,
        password=generate_password_hash(admin_password),
        is_admin=True
    )

    db.session.add(admin_user)
    db.session.commit()
    print(f"✅ Admin user '{admin_email}' created successfully.")

def main():
    """Main entry point to run inside Flask app context."""
    app = create_app()
    with app.app_context():
        try:
            create_admin()
        except Exception as e:
            db.session.rollback()
            print("❌ Error occurred while creating admin user:", e)

# Only execute if this script is run directly (not imported)
if __name__ == "__main__":
    main()