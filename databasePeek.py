from app import create_app, db
from app.models import User, Ticket

# Ensure we connect to the same app instance
app = create_app()
app.app_context().push()

# Peek at users
users = User.query.all()
print(users)  # Print users on the db

for u in User.query.all():  # Print user ids, emails, is_admin flag
    print(u.id, u.email, u.is_admin)