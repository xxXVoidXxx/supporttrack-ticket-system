# SupportTrack Ticket System

SupportTrack is a Flask-based help desk and ticket management system designed for IT support teams, admin operations, or small businesses needing a lightweight internal support tool.

It includes full user authentication, an admin dashboard with ticket filtering and export tools, and a clean Bootstrap interface.

---

## 🚀 Features

### ✅ User Functionality
- Register and log in securely
- Submit support tickets with title and description
- View personal ticket history
- Status updates shown in real-time

### 🛠️ Admin Functionality
- View all submitted tickets
- Filter tickets by status (Open, In Progress, Closed)
- Update ticket statuses from the dashboard
- Export all tickets as CSV
- Manage users (promote/demote admin rights)

### 🎨 UI & Framework
- Responsive layout with [Bootstrap 5](https://getbootstrap.com/)
- Flash message alerts for user feedback
- Admin tools are cleanly organized for efficiency

---

## 🏗️ Technologies Used

- Python 3
- Flask (with Blueprints and Factory Pattern)
- Flask-Login
- Flask-WTF (form handling + CSRF protection)
- SQLite (default, easily swappable)
- Bootstrap 5 (via CDN)
- Git/GitHub for version control

---

## ⚙️ Setup Instructions

1. **Clone the repo:**
   ```bash
   git clone https://github.com/xxXVoidXxx/supporttrack-ticket-system.git
   cd supporttrack-ticket-system
   ```

2. **Create & activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate    # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   python run.py
   ```

5. **Create an admin user:**
   ```bash
   python create_admin.py
   ```

---

## 📦 Deployment-Ready

This project is ready to be deployed to services like [Render](https://render.com), [Railway](https://railway.app), or [Fly.io](https://fly.io). The application pulls configuration using environment variables and can easily be adapted for cloud databases or other environments.

---

## 🔐 Demo Credentials

Use the following test account to explore the full admin functionality:

**Admin Login**  
📧 Email: `admin@example.com`  
🔑 Password: `YourSecurePassword123!`

This account grants access to:
- Admin Dashboard
- Ticket status updates
- User management panel
- CSV export and filter tools

If deploying, be sure to run `create_admin.py` to initialize this account.

---

## 🧪 Optional: Seeding the Database

If you want to populate the app with clean demo data (users + tickets), run the included `seed_data.py` script:

```bash
python seed_data.py

---

## 📫 Contact

Built with ❤️ by [@xxXVoidXxx](https://github.com/xxXVoidXxx)  
Open to feedback, collaboration, or ideas.

Feel free to open an issue or reach out via GitHub!