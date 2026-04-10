# Student Attendance & Engagement Tracker - Streamlit Version

A comprehensive web application for tracking student attendance and engagement, built with Streamlit and SQLite.

## Features

### For Students
- 📊 View personal attendance dashboard
- 📈 Track engagement records
- 📤 Export personal data
- ⚙️ Change password

### For Teachers
- 📝 Mark student attendance
- 💬 Record student engagement
- 👥 View all students
- 📊 View analytics dashboard
- 📤 Export attendance/engagement reports

### For Admins
- 🎓 All teacher features
- ➕ Add/manage students
- 📤 Bulk upload students (CSV)
- 👨‍🏫 Manage teachers
- 📊 System-wide analytics
- 📤 Export all reports

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/student-tracker.git
cd student-tracker
```

2. **Create virtual environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements_streamlit.txt
```

4. **Run the app**
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501/`

## Database Setup

The app uses SQLite database which is automatically initialized. The database includes:

- **Users**: Student, Teacher, and Admin accounts
- **Subjects**: List of courses/subjects
- **Attendance**: Student attendance records
- **Engagement**: Student engagement/behavior records

## Demo Credentials

```
Admin:
  Email: admin@example.com
  Password: Admin@123

Teacher:
  Email: teacher1@example.com
  Password: Teacher@123

Student:
  Email: student1@example.com
  Password: Student@123
```

## Deployment

### Deploy to Streamlit Cloud

1. **Push code to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Go to Streamlit Cloud** (https://streamlit.io/cloud)

3. **Click "New app"** and connect your GitHub repository

4. **Select**:
   - Repository: your-username/student-tracker
   - Main file path: streamlit_app.py
   - Python version: 3.9

5. **Click "Deploy"**

### Deploy to Other Platforms

The app can also be deployed to:
- Heroku
- AWS
- DigitalOcean
- Azure
- Google Cloud

## Folder Structure

```
student-tracker/
├── streamlit_app.py          # Main Streamlit app
├── models.py                 # Database models
├── generate_data.py          # Data generation script
├── requirements_streamlit.txt # Dependencies
├── attendance.db             # SQLite database
├── README_STREAMLIT.md       # This file
└── .gitignore               # Git ignore rules
```

## Usage

### For Marking Attendance
1. Login as Teacher or Admin
2. Go to "Attendance" section
3. Select student, subject, date, and status
4. Click "Save Attendance"

### For Recording Engagement
1. Login as Teacher or Admin
2. Go to "Engagement" section
3. Select student, subject, tag, and optional note
4. Click "Save Engagement"

### For Exporting Data
1. Login
2. Go to "Export" section
3. Choose export type
4. Click download button

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements_streamlit.txt
```

### Database locked error
- Close other instances of the app
- Delete `attendance.db` and restart to reinitialize

### Port already in use
```bash
streamlit run streamlit_app.py --server.port 8502
```

## Development

### Generate test data
```bash
python generate_data.py
```

### Database migrations
Edit `models.py` and run:
```bash
python -c "from models import *; db.create_all()"
```

## API Endpoints (Flask version)

For the original Flask version, see the main README.md

## License

MIT License - feel free to use this project for personal or commercial use.

## Support

For issues and feature requests, please create a GitHub issue.

## Contributors

- Your Name (@username)

---

**Last Updated:** April 2026
