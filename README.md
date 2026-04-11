# Student Tracker - Streamlit Edition

A comprehensive student attendance and engagement tracking system built with **Streamlit** and **SQLAlchemy**.

✅ **FREE DEPLOYMENT** - Hosted on Hugging Face Spaces (no payment ever required!)

## 🚀 Quick Access

**Live App**: [https://huggingface.co/spaces/YOUR_USERNAME/student-tracker](https://huggingface.co/spaces/YOUR_USERNAME/student-tracker)

## Features

📊 **Dashboard** - View attendance and engagement metrics  
📝 **Attendance Tracking** - Record student attendance by subject  
💬 **Engagement Tracking** - Track student engagement with notes and tags  
👥 **Student Management** - Manage student information and records  
🔐 **Role-Based Access** - Admin, Teacher, and Student roles with different permissions  
📱 **User Settings** - Manage user profile information  

## 👥 User Roles & Access

| Feature | Admin | Teacher | Student |
|---------|-------|---------|---------|
| View Dashboard | ✅ | ✅ | ✅ |
| Record Attendance | ✅ | ✅ | ❌ |
| Record Engagement | ✅ | ✅ | ❌ |
| View All Students | ✅ | ✅ | ❌ |
| Manage Students | ✅ | ❌ | ❌ |
| View Settings | ✅ | ✅ | ✅ |

## Tech Stack

- **Frontend & Backend**: Streamlit
- **Database**: SQLAlchemy ORM + SQLite
- **Hosting**: Hugging Face Spaces
- **Language**: Python 3.11

## Project Structure

```
student-tracker/
├── streamlit_app.py      # Main Streamlit application
├── models.py             # SQLAlchemy database models
├── requirements.txt      # Python dependencies
├── attendance.db         # SQLite database
├── README.md            # This file
└── HUGGINGFACE_DEPLOY.md # Deployment guide
    ├── signup.html       # Registration form
    ├── dashboard.html    # Main dashboard with 3 charts (Chart.js)
    ├── attendance.html   # Record attendance form
    ├── engagement.html   # Record engagement form
    ├── students.html     # Students list with pagination and search
    ├── student_detail.html # Individual student view with tabs
    ├── settings.html     # User settings and about
    ├── 404.html         # Error page
    └── 500.html         # Server error page
```

## Quick Start - Deploy in 5 Minutes ⚡

### Online (Free) - Hugging Face Spaces

1. **Push to GitHub** (already done!)
2. **Go to**: https://huggingface.co/new-space
3. **Create new Space**:
   - Name: `student-tracker`
   - SDK: Select **Streamlit**
   - Visibility: Public or Private
4. **Connect GitHub Repository**:
   - Select `chitransh24god/student-tracker`
   - Branch: `main`
5. **Wait 2-3 minutes** ⏳
6. **Your app is live!** 🎉

📖 **Full guide**: See [HUGGINGFACE_DEPLOY.md](HUGGINGFACE_DEPLOY.md)

### Local Development

**Prerequisites**: Python 3.11+

**Step 1: Clone**
```bash
git clone https://github.com/chitransh24god/student-tracker
cd student-tracker
```

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Run**
```bash
streamlit run streamlit_app.py
```

Open browser at: **http://localhost:8501**

## Demo Accounts

Pre-configured test accounts available:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | Admin@123 |
| Teacher | teacher@example.com | Teacher@123 |
| Student | student@example.com | Student@123 |

## Features Breakdown

### 📊 Dashboard Page
- Quick stats cards (attendance %, daily average)
- Last 7 days attendance summary
- View engagement records

### 📝 Attendance Management  
- Record attendance by student, subject, and date
- Mark as Present/Absent/Leave
- View attendance history
- Search and filter options

### 💬 Engagement Tracking
- Record engagement scores
- Add detailed notes
- Tag engagement (e.g., "Excellent", "Needs Help")
- Filter by date range

### 👥 Student Management (Admin Only)
- View all student details
- Add new students
- Edit student information
- Deactivate/reactivate students

### ⚙️ Settings & Profile
- View personal information
- Update password
- View role and permissions

## Environment Setup

### Required Environment Variables
None! The app works out of the box with SQLite.

### Optional Configuration
Edit `.streamlit/config.toml` for custom settings:
```toml
[theme]
primaryColor = "#FF6B6B"

[server]
maxUploadSize = 200
```

## Database

- **Type**: SQLite (lightweight, no server needed)
- **File**: `attendance.db`
- **Auto-init**: Database initializes automatically with sample data on first run
- **Persistence**: Data persists between app restarts

## Deployment

### Hugging Face Spaces (Recommended - Free)
✅ Automatically deploys from GitHub  
✅ Always online, no cold starts  
✅ Free SQL ite database support  
✅ Visit: https://huggingface.co/spaces/YOUR_USERNAME/student-tracker

### Local Deployment
```bash
git push origin main
# If repo is connected to Hugging Face Spaces, it auto-deploys!
```

## Troubleshooting

**App won't load?**
- Clear browser cache
- Restart Streamlit: `streamlit run streamlit_app.py --logger.level=debug`

**Database errors?**
- Delete `attendance.db` to reset
- App will recreate with sample data

**Login not working?**
- Check you're using correct credentials from demo accounts table above
- Password is case-sensitive

**Performance issues?**
- Switch to non-debug mode on Hugging Face Spaces
- Database queries are optimized for SQLite

## Support & Documentation

- Streamlit Docs: https://docs.streamlit.io
- Hugging Face: https://huggingface.co
- GitHub Issues: Report bugs in repository

## License

This project is provided as-is for educational purposes.

You can:
1. Sign in with these credentials to explore faculty features
2. Create a new student account during registration
3. Record attendance and engagement data

## Default Subjects

The following subjects are pre-loaded:
- Mathematics
- Physics
- Chemistry
- English
- Programming
- Database Design

## Usage Guide

### For Faculty

1. **Record Attendance**
   - Navigate to "Add Attendance"
   - Select student, subject, date, and status (Present/Absent)
   - Submit to record (duplicate prevention built-in)

2. **Add Engagement Notes**
   - Navigate to "Add Engagement"
   - Select student, subject, date
   - Choose engagement tag (Active Participation, Excellent Work, etc.)
   - Add optional detailed notes
   - Submit

3. **View Student Records**
   - Navigate to "Students"
   - Use search to filter students by name/email
   - Click "View Details" on any student
   - See attendance history and engagement records
   - View individual student statistics

4. **Export Data**
   - Click "Export Data" in navbar
   - Downloads CSV with all attendance and engagement records

### For Students

1. **View Dashboard**
   - Login with your credentials
   - See your attendance statistics (Total Classes, Attended, Percentage)
   - View attendance trends by subject
   - Track engagement records
   - See monthly trends

## Database Models

### User
- id (Primary Key)
- name (String)
- email (Unique)
- password_hash (Hashed with Werkzeug)
- role (faculty/student)
- created_at (DateTime)

### Subject
- id (Primary Key)
- name (String, Unique)
- created_at (DateTime)

### Attendance
- id (Primary Key)
- student_id (Foreign Key to User)
- subject_id (Foreign Key to Subject)
- date (Date)
- status (Present/Absent)
- created_at (DateTime)
- **Unique Constraint**: (student_id, subject_id, date) - prevents duplicate entries

### Engagement
- id (Primary Key)
- student_id (Foreign Key to User)
- subject_id (Foreign Key to Subject)
- date (Date)
- tag (String)
- note (Text, Optional)
- created_at (DateTime)

## API Endpoints

### Public Routes
- `GET /` - Home (redirects to dashboard or login)
- `GET /login` - Login page
- `POST /login` - Login submission
- `GET /signup` - Signup page
- `POST /signup` - Registration submission
- `GET /logout` - Logout

### Protected Routes (Login Required)
- `GET /dashboard` - Main dashboard with statistics
- `GET /export` - Export data to CSV
- `GET /settings` - User settings page

### Faculty Only Routes
- `GET /attendance` - Attendance form
- `POST /attendance` - Record attendance
- `GET /engagement` - Engagement form
- `POST /engagement` - Record engagement
- `GET /students` - View all students (paginated)
- `GET /student/<id>` - View student details

### API Endpoints (JSON)
- `GET /api/attendance-by-subject` - Chart data for attendance by subject
- `GET /api/monthly-trend` - Chart data for monthly attendance trend
- `GET /api/engagement-distribution` - Chart data for engagement tags

## Configuration

Edit the following in `app.py` for production:

```python
# Change this to a strong secret key in production
app.config['SECRET_KEY'] = 'your_secret_key_change_in_production'

# Database path (default: SQLite in project directory)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'

# Debug mode (set to False in production)
app.run(debug=True)
```

## Design Highlights

### Professional Light Theme
- Clean white and soft gray color scheme
- Blue accent colors (#4F46E5) with secondary colors
- Responsive grid layouts with CSS Grid and Flexbox
- Smooth transitions and hover effects
- Professional typography with Poppins font (Google Fonts)

### Components
- Sticky navigation bar with role-aware menu
- Auto-dismiss flash messages with animations
- Responsive statistics cards with hover effects
- Professional data tables with striped rows
- Interactive Chart.js visualizations (Bar, Line, Pie)
- Tab interface for organized content
- Form validation client-side and server-side

### Responsive Design
- Mobile-first approach
- Breakpoints: 1400px (desktop), 768px (tablet), 480px (mobile)
- Flexible grid layouts
- Touch-friendly buttons and inputs
- Optimized for all screen sizes

## Security Features

- ✅ Password hashing with Werkzeug (not plain text)
- ✅ Secure session management
- ✅ Role-based access control (RBAC)
- ✅ HTTP-only session cookies
- ✅ CSRF protection ready (Flask session)
- ✅ Input validation (server-side)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS protection (Jinja2 auto-escaping)

## Performance Optimizations

- Efficient database queries with SQLAlchemy
- Pagination for student lists
- Client-side search filtering
- Lazy-loaded charts
- Optimized CSS with variables and modern techniques
- Minified JavaScript (production-ready)

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py:
app.run(port=5001)
```

### Database Issues
Delete `attendance.db` to reset database:
```bash
rm attendance.db  # Linux/Mac
del attendance.db  # Windows
```

### Import Errors
Ensure all packages are installed:
```bash
pip install -r requirements.txt
```

### Module Not Found
Make sure you're in the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

## Browser Compatibility

- Chrome/Edge (Latest)
- Firefox (Latest)
- Safari (Latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Deployment Options

1. **Heroku**: Add Procfile and requirements.txt
2. **PythonAnywhere**: Web hosting platform for Python apps
3. **AWS EC2**: Deploy with Gunicorn and Nginx
4. **DigitalOcean**: VPS deployment
5. **Docker**: Containerize the application

## Future Enhancements

- Email notifications for attendance alerts
- User profile pictures and customization
- Advanced analytics and reports
- Mobile application
- SMS notifications
- Parent/Guardian portal
- Dark mode theme
- Two-factor authentication
- Bulk import from CSV
- Calendar view for attendance

## Code Quality

- Clean, modular architecture
- Comprehensive comments and docstrings
- Follows Flask best practices
- SQLAlchemy ORM for database operations
- Responsive HTML structure
- CSS organized with variables and sections
- JavaScript with proper error handling

## Support & License

This application is provided as-is for educational purposes. Feel free to modify and extend for your needs.

---

**Version:** 1.0.0
**Created:** 2024
**Last Updated:** 2024
