# seed_data.py
# This script resets the SupportTrack database to a clean, professional demo state.
# It removes all existing users and tickets, then inserts fresh, minimal seed data.

from app import create_app, db
from app.models import User, Ticket
from werkzeug.security import generate_password_hash

# Create the Flask app and push the application context
app = create_app()

with app.app_context():
    # Step 1: Clear all existing data
    print("🧹 Resetting database...")
    Ticket.query.delete()
    User.query.delete()
    db.session.commit()

    # Step 2: Create users
    print("👤 Creating users...")

    # Admin user
    admin = User(
        email="admin@example.com",
        password=generate_password_hash("YourSecurePassword123!"),
        is_admin=True
    )

    # Standard users
    user1 = User(
        email="jane.doe@example.com",
        password=generate_password_hash("userpassword1"),
        is_admin=False
    )
    user2 = User(
        email="john.smith@example.com",
        password=generate_password_hash("userpassword2"),
        is_admin=False
    )

    db.session.add_all([admin, user1, user2])
    db.session.commit()

    # Step 3: Create tickets
    print("📩 Adding demo tickets...")

    ticket1 = Ticket(
        title="VPN Access Request",
        description="User unable to connect to VPN after password reset.",
        status="Open",
        author=user1
    )
    ticket2 = Ticket(
        title="Software Installation",
        description="Requesting install of VS Code on new laptop.",
        status="In Progress",
        author=user2
    )
    ticket3 = Ticket(
        title="Monitor Not Working",
        description="External monitor not detected when docking.",
        status="Closed",
        author=user1
    )

    db.session.add_all([ticket1, ticket2, ticket3])
    db.session.commit()

    print("✅ Database seeded successfully.")
