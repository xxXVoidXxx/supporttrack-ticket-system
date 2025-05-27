# Import core Flask utilities
from flask import Blueprint, render_template, redirect, url_for, flash, request

# Import login system tools
from flask_login import login_user, logout_user, current_user, login_required

# Import our form classes from forms.py
from app.forms import LoginForm, RegistrationForm, TicketForm

# Import our database models
from app.models import User, Ticket

# Import the database session
from app import db

# Import password utilities
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the route blueprint
bp = Blueprint('routes', __name__)

# -------------------------------
# Route: Homepage
# -------------------------------
@bp.route('/')
def index():
    return redirect(url_for('routes.login'))

# -------------------------------
# Route: Login
# -------------------------------
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect them to their dashboard
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))

    # Create a new instance of the login form
    form = LoginForm()

    # Check if the form was submitted and validated successfully
    if form.validate_on_submit():
        # Try to find a user in the database by the submitted email
        user = User.query.filter_by(email=form.email.data).first()

        # If a user exists and the password matches the hashed version
        if user and check_password_hash(user.password, form.password.data):
            # Log the user in and optionally remember their session
            login_user(user, remember=form.remember.data)

            # Flash a success message to confirm login
            flash('Login successful.', 'success')

            # Redirect based on user role: admins to admin dashboard, users to user dashboard
            if user.is_admin:
                return redirect(url_for('routes.admin_dashboard'))
            else:
                return redirect(url_for('routes.dashboard'))
        else:
            # If login failed, flash an error message
            flash('Invalid email or password.', 'danger')

    # Render the login page with the form (GET request or failed POST)
    return render_template('login.html', form=form)
    

# -------------------------------
# Route: Registration
# -------------------------------
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)

# -------------------------------
# Route: Logout
# -------------------------------
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))

# -------------------------------
# Route: User Dashboard
# -------------------------------
@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            author=current_user
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket submitted successfully.', 'success')
        return redirect(url_for('routes.dashboard'))

    tickets = Ticket.query.filter_by(user_id=current_user.id)\
        .order_by(Ticket.timestamp.desc()).all()

    return render_template('dashboard.html', form=form, tickets=tickets)

# -------------------------------
# Route: Admin Dashboard
# -------------------------------
@bp.route('/admin')
@login_required
def admin_dashboard():
    # Only allow access for admin users
    if not current_user.is_admin:
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('routes.dashboard'))

    # Get the selected filter from the query string (GET param)
    status_filter = request.args.get('status')

    # If a status is selected, filter tickets by that
    if status_filter in ['Open', 'In Progress', 'Closed']:
        tickets = Ticket.query.filter_by(status=status_filter)\
            .order_by(Ticket.timestamp.desc()).all()
    else:
        # Otherwise show all tickets
        tickets = Ticket.query.order_by(Ticket.timestamp.desc()).all()

    return render_template('admin_dashboard.html', tickets=tickets)


# -------------------------------
# Route: Update Ticket Status (Admins only)
# -------------------------------
@bp.route('/update_status/<int:ticket_id>', methods=['POST'])
@login_required
def update_status(ticket_id):
    if not current_user.is_admin:
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('routes.dashboard'))

    ticket = Ticket.query.get_or_404(ticket_id)
    new_status = request.form.get('status')

    if new_status in ['Open', 'In Progress', 'Closed']:
        ticket.status = new_status
        db.session.commit()
        flash(f'Ticket #{ticket.id} status updated to "{new_status}".', 'success')
    else:
        flash('Invalid status selection.', 'danger')

    return redirect(url_for('routes.admin_dashboard'))


# -------------------------------
# Route: Export Tickets as CSV (Admins only)
# -------------------------------
@bp.route('/export_tickets')
@login_required
def export_tickets():
    # Only allow admin access
    if not current_user.is_admin:
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('routes.dashboard'))

    # Query all tickets
    tickets = Ticket.query.order_by(Ticket.timestamp.desc()).all()

    # Import CSV and IO modules to generate file in memory
    import csv
    from io import StringIO
    from flask import Response

    # Create a memory stream to hold the CSV
    si = StringIO()
    writer = csv.writer(si)

    # Write header row
    writer.writerow(['ID', 'Title', 'Description', 'Status', 'Author', 'Timestamp'])

    # Write each ticket as a row
    for t in tickets:
        writer.writerow([
            t.id,
            t.title,
            t.description,
            t.status,
            t.author.email,
            t.timestamp.strftime('%Y-%m-%d %H:%M')
        ])

    # Return the CSV file as a downloadable response
    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=tickets_export.csv"
    return output



# -------------------------------
# Route: User Management (Admins only)
# -------------------------------
@bp.route('/users')
@login_required
def user_management():
    # Ensure only admins can access this
    if not current_user.is_admin:
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('routes.dashboard'))

    # Get all registered users from the database
    users = User.query.order_by(User.id).all()

    # Render the user management panel
    return render_template('user_management.html', users=users)



# -------------------------------
# Route: Toggle Admin Status (Admins only)
# -------------------------------
@bp.route('/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
def toggle_admin(user_id):
    # Only admins can use this
    if not current_user.is_admin:
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('routes.dashboard'))

    user = User.query.get_or_404(user_id)

    # Prevent admins from demoting themselves
    if user.id == current_user.id:
        flash("You cannot change your own admin status.", "warning")
        return redirect(url_for('routes.user_management'))

    # Flip admin status
    user.is_admin = not user.is_admin
    db.session.commit()

    status = "promoted to admin" if user.is_admin else "demoted to user"
    flash(f"{user.email} has been {status}.", "success")
    return redirect(url_for('routes.user_management'))
