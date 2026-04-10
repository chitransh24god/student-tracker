from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from models import db, User, Subject, Attendance, Engagement
from functools import wraps
from datetime import datetime, timedelta
import csv
from io import StringIO
from sqlalchemy import func, case
import os
import random
import string

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_change_in_production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize database
db.init_app(app)

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for faculty only
def faculty_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if user.role not in ['faculty', 'teacher', 'admin']:
            flash('Access denied. Faculty/Teacher/Admin only.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for admin only
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if user.role != 'admin':
            flash('Access denied. Admin only.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request():
    """Make user info available in all templates"""
    if 'user_id' in session:
        g_user = User.query.get(session['user_id'])
        if g_user:
            g_user_info = {'id': g_user.id, 'name': g_user.name, 'role': g_user.role}


# Helper function to generate random students
def generate_random_students(count=50):
    """Generate random student data"""
    first_names = ['Alex', 'Jordan', 'Casey', 'Morgan', 'Riley', 'Taylor', 'Avery', 'Quinn', 
                   'Jamie', 'Sam', 'Parker', 'Drew', 'Blake', 'Sage', 'Sky', 'River', 'Cameron', 
                   'Dakota', 'Phoenix', 'Dakota', 'Tatum', 'Bailey', 'Charlie', 'Devon', 'Finley',
                   'Harley', 'Indigo', 'Jayden', 'Kai', 'Logan', 'Morgan', 'Noah', 'Oakley',
                   'Parker', 'Quinn', 'Riley', 'Sage', 'Taylor', 'Umber', 'Vale', 'Whitney',
                   'Xavier', 'Yale', 'Zephyr', 'Aiden', 'Bowen', 'Carter', 'Dylan', 'Elliott',
                   'Finley', 'Greyson', 'Henry']
    
    last_names = ['Johnson', 'Smith', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                  'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
                  'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
                  'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Young',
                  'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Peterson', 'Phillips', 'Campbell',
                  'Parker', 'Evans', 'Edwards', 'Collins', 'Reeves', 'Stewart', 'Morris', 'Rogers',
                  'Morgan', 'Peterson', 'Cooper', 'Reed']
    
    students = []
    for i in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        email = f"student{i+1}@example.com"
        
        # Check if student already exists
        if not User.query.filter_by(email=email).first():
            student = User(name=name, email=email, role='student')
            student.set_password('student123')  # Default password
            students.append(student)
    
    return students


def generate_random_teachers(count=10):
    """Generate random teacher data"""
    first_names = ['Dr. David', 'Prof. Sarah', 'Dr. Michael', 'Prof. Jennifer', 'Dr. Robert',
                   'Prof. Emily', 'Dr. James', 'Prof. Amanda', 'Dr. William', 'Prof. Lisa',
                   'Dr. Charles', 'Prof. Margaret', 'Dr. Daniel', 'Prof. Patricia']
    
    last_names = ['Johnson', 'Smith', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                  'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson']
    
    teachers = []
    for i in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        email = f"teacher{i+1}@example.com"
        
        # Check if teacher already exists
        if not User.query.filter_by(email=email).first():
            teacher = User(name=name, email=email, role='teacher')
            teacher.set_password('teacher123')  # Default password
            teachers.append(teacher)
    
    return teachers


def generate_sample_attendance_engagement():
    """Generate 6 months of sample attendance and engagement data"""
    students = User.query.filter_by(role='student').all()
    subjects = Subject.query.all()
    
    if not students or not subjects:
        return
    
    print('[INFO] Starting data generation for %d students and %d subjects...' % (len(students), len(subjects)))
    
    # Generate data for past 6 months
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=180)
    
    engagement_tags = [
        'Active Participation', 'Late Submission', 'Disruptive',
        'Excellent Work', 'Improvement Needed', 'Helps Peers', 'Creative Thinking'
    ]
    
    attendance_records = []
    engagement_records = []
    
    # Generate attendance records
    current_date = start_date
    day_count = 0
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() < 5:
            # Select 70% of students for each day
            selected_students = random.sample(students, max(1, int(len(students) * 0.7)))
            
            for subject in subjects:
                for student in selected_students:
                    status = 'Present' if random.random() < 0.85 else 'Absent'
                    attendance = Attendance(
                        student_id=student.id,
                        subject_id=subject.id,
                        date=current_date,
                        status=status
                    )
                    attendance_records.append(attendance)
        
        current_date += timedelta(days=1)
        day_count += 1
        
        if day_count % 30 == 0:
            print('[INFO] Processed %d days of attendance...' % day_count)
    
    # Add all attendance records
    if attendance_records:
        for record in attendance_records:
            db.session.add(record)
        db.session.commit()
        print('[OK] Generated %d attendance records' % len(attendance_records))
    
    # Generate engagement records
    for student in students:
        for _ in range(random.randint(15, 30)):
            random_date = start_date + timedelta(days=random.randint(0, 180))
            tag = random.choice(engagement_tags)
            note = 'Good participation in class'
            
            engagement = Engagement(
                student_id=student.id,
                subject_id=random.choice(subjects).id,
                date=random_date,
                tag=tag,
                note=note
            )
            engagement_records.append(engagement)
    
    # Add all engagement records
    if engagement_records:
        for record in engagement_records:
            db.session.add(record)
        db.session.commit()
        print('[OK] Generated %d engagement records' % len(engagement_records))


@app.route('/', methods=['GET', 'POST'])
def index():
    """Home page - redirect to dashboard or login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'student')
        
        # Validation
        if not name or not email or not password:
            flash('All fields are required', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('signup'))
        
        # Create new user
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration', 'danger')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', '').strip()
        
        if not email or not password or not role:
            flash('Email, password, and role are required', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            # Check if user's role matches selected role
            if user.role != role:
                flash('Invalid role for this account', 'danger')
                return redirect(url_for('login'))
            
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash(f'Welcome {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - shows statistics and charts"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if user.role in ['faculty', 'teacher', 'admin']:
        # Faculty/Teacher/Admin dashboard shows overview of all students
        total_students = User.query.filter_by(role='student').count()
        total_teachers = User.query.filter_by(role='teacher').count()
        total_attendance_records = Attendance.query.count()
        total_engagement_records = Engagement.query.count()
        total_subjects = Subject.query.count()
        
        stats = {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_attendance_records': total_attendance_records,
            'total_engagement_records': total_engagement_records,
            'total_subjects': total_subjects
        }
    else:
        # Student dashboard shows their own stats
        total_classes = Attendance.query.filter_by(student_id=user_id).count()
        
        attended = Attendance.query.filter_by(
            student_id=user_id,
            status='Present'
        ).count()
        
        attendance_percentage = ((attended / total_classes * 100) if total_classes > 0 else 0)
        
        total_engagement = Engagement.query.filter_by(student_id=user_id).count()
        
        stats = {
            'total_classes': total_classes,
            'attended': attended,
            'attendance_percentage': round(attendance_percentage, 1),
            'total_engagement': total_engagement
        }
    
    return render_template('dashboard.html', user=user, stats=stats)


@app.route('/attendance', methods=['GET', 'POST'])
@faculty_required
def attendance():
    """Attendance management page"""
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject_id = request.form.get('subject_id')
        date_str = request.form.get('date')
        status = request.form.get('status')
        
        # Validation
        if not all([student_id, subject_id, date_str, status]):
            flash('All fields are required', 'danger')
            return redirect(url_for('attendance'))
        
        try:
            attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(url_for('attendance'))
        
        # Check for duplicate
        existing = Attendance.query.filter_by(
            student_id=student_id,
            subject_id=subject_id,
            date=attendance_date
        ).first()
        
        if existing:
            flash('Attendance already recorded for this student on this date', 'warning')
            return redirect(url_for('attendance'))
        
        # Create attendance record
        attendance_record = Attendance(
            student_id=student_id,
            subject_id=subject_id,
            date=attendance_date,
            status=status
        )
        
        try:
            db.session.add(attendance_record)
            db.session.commit()
            flash('Attendance recorded successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error recording attendance', 'danger')
        
        return redirect(url_for('attendance'))
    
    students = User.query.filter_by(role='student').all()
    subjects = Subject.query.all()
    
    # Fetch recent attendance records
    recent_records = db.session.query(
        User.name,
        Subject.name,
        Attendance.date,
        Attendance.status
    ).join(User, Attendance.student_id == User.id).join(
        Subject, Attendance.subject_id == Subject.id
    ).order_by(Attendance.date.desc()).limit(10).all()
    
    return render_template('attendance.html', students=students, subjects=subjects, recent_records=recent_records)


@app.route('/engagement', methods=['GET', 'POST'])
@faculty_required
def engagement():
    """Engagement tracking page"""
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject_id = request.form.get('subject_id')
        date_str = request.form.get('date')
        tag = request.form.get('tag')
        note = request.form.get('note', '')
        
        # Validation
        if not all([student_id, subject_id, date_str, tag]):
            flash('All required fields must be filled', 'danger')
            return redirect(url_for('engagement'))
        
        try:
            engagement_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(url_for('engagement'))
        
        # Create engagement record
        engagement_record = Engagement(
            student_id=student_id,
            subject_id=subject_id,
            date=engagement_date,
            tag=tag,
            note=note
        )
        
        try:
            db.session.add(engagement_record)
            db.session.commit()
            flash('Engagement record created successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error creating engagement record', 'danger')
        
        return redirect(url_for('engagement'))
    
    students = User.query.filter_by(role='student').all()
    subjects = Subject.query.all()
    tags = [
        'Active Participation',
        'Late Submission',
        'Disruptive',
        'Excellent Work',
        'Improvement Needed',
        'Helps Peers',
        'Creative Thinking'
    ]
    
    return render_template('engagement.html', students=students, subjects=subjects, tags=tags)


@app.route('/api/attendance-by-subject')
@login_required
def api_attendance_by_subject():
    """API endpoint for attendance by subject chart"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    try:
        query = db.session.query(
            Subject.name,
            func.sum(case((Attendance.status == 'Present', 1), else_=0)).label('present'),
            func.count(Attendance.id).label('total')
        ).join(Attendance, Subject.id == Attendance.subject_id).group_by(Subject.id, Subject.name)
        
        if user.role == 'student':
            query = query.filter(Attendance.student_id == user_id)
        
        results = query.all()
        
        data = {
            'labels': [r[0] for r in results],
            'present': [r[1] or 0 for r in results],
            'total': [r[2] for r in results],
            'percentages': [
                round((r[1] or 0) / r[2] * 100) if r[2] > 0 else 0
                for r in results
            ]
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e), 'labels': [], 'percentages': []}), 500


@app.route('/api/monthly-trend')
@login_required
def api_monthly_trend():
    """API endpoint for monthly attendance trend"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    try:
        # Get last 6 months of data
        six_months_ago = datetime.now().date() - timedelta(days=180)
        
        query = db.session.query(
            func.strftime('%Y-%m', Attendance.date).label('month'),
            func.sum(case((Attendance.status == 'Present', 1), else_=0)).label('present'),
            func.count(Attendance.id).label('total')
        ).filter(Attendance.date >= six_months_ago).group_by(
            func.strftime('%Y-%m', Attendance.date)
        )
        
        if user.role == 'student':
            query = query.filter(Attendance.student_id == user_id)
        
        results = query.order_by('month').all()
        
        data = {
            'labels': [r[0] for r in results],
            'present': [r[1] or 0 for r in results],
            'total': [r[2] for r in results],
            'percentages': [
                round((r[1] or 0) / r[2] * 100) if r[2] > 0 else 0
                for r in results
            ]
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e), 'labels': [], 'percentages': []}), 500


@app.route('/api/engagement-distribution')
@login_required
def api_engagement_distribution():
    """API endpoint for engagement tag distribution"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    query = db.session.query(
        Engagement.tag,
        func.count(Engagement.id).label('count')
    ).group_by(Engagement.tag)
    
    if user.role == 'student':
        query = query.filter(Engagement.student_id == user_id)
    
    results = query.all()
    
    data = {
        'labels': [r[0] for r in results],
        'counts': [r[1] for r in results]
    }
    
    return jsonify(data)


@app.route('/export')
@login_required
def export():
    """Export attendance and engagement data to CSV"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    # Prepare CSV data
    output = StringIO()
    
    # Attendance Export
    output.write('=== ATTENDANCE RECORDS ===\n')
    output.write('Student Name,Email,Subject,Date,Status\n')
    
    attendance_query = Attendance.query.join(User).join(Subject)
    if user.role == 'student':
        attendance_query = attendance_query.filter(Attendance.student_id == user_id)
    
    for record in attendance_query.all():
        output.write(f'{record.student.name},{record.student.email},{record.subject.name},{record.date},{record.status}\n')
    
    output.write('\n=== ENGAGEMENT RECORDS ===\n')
    output.write('Student Name,Email,Subject,Date,Tag,Note\n')
    
    engagement_query = Engagement.query.join(User).join(Subject)
    if user.role == 'student':
        engagement_query = engagement_query.filter(Engagement.student_id == user_id)
    
    for record in engagement_query.all():
        note = record.note.replace(',', ';').replace('\n', ' ') if record.note else ''
        output.write(f'{record.student.name},{record.student.email},{record.subject.name},{record.date},{record.tag},"{note}"\n')
    
    # Return as downloadable file
    csv_data = output.getvalue()
    
    from flask import make_response
    response = make_response(csv_data)
    response.headers['Content-Disposition'] = f'attachment; filename=attendance_engagement_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response.headers['Content-Type'] = 'text/csv'
    
    return response


@app.route('/students')
@faculty_required
def students():
    """View all students"""
    page = request.args.get('page', 1, type=int)
    students_list = User.query.filter_by(role='student').paginate(page=page, per_page=10)
    return render_template('students.html', students=students_list)


@app.route('/student/<int:student_id>')
@faculty_required
def student_detail(student_id):
    """View student details"""
    student = User.query.get_or_404(student_id)
    
    if student.role != 'student':
        flash('Invalid student', 'danger')
        return redirect(url_for('students'))
    
    attendance_records = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).all()
    engagement_records = Engagement.query.filter_by(student_id=student_id).order_by(Engagement.date.desc()).all()
    
    total_classes = len(attendance_records)
    attended = sum(1 for a in attendance_records if a.status == 'Present')
    attendance_percentage = (attended / total_classes * 100) if total_classes > 0 else 0
    
    return render_template('student_detail.html', 
                         student=student, 
                         attendance_records=attendance_records,
                         engagement_records=engagement_records,
                         total_classes=total_classes,
                         attended=attended,
                         attendance_percentage=round(attendance_percentage, 1))


@app.route('/settings')
@login_required
def settings():
    """User settings page"""
    user = User.query.get(session['user_id'])
    return render_template('settings.html', user=user)


@app.route('/admin/add-student', methods=['GET', 'POST'])
@admin_required
def admin_add_student():
    """Admin only: Add new student"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        if not name or not email or not password:
            flash('All fields are required', 'danger')
            return redirect(url_for('admin_add_student'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('admin_add_student'))
        
        # Create new student
        student = User(name=name, email=email, role='student')
        student.set_password(password)
        
        try:
            db.session.add(student)
            db.session.commit()
            flash(f'Student {name} added successfully!', 'success')
            return redirect(url_for('admin_add_student'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding student', 'danger')
            return redirect(url_for('admin_add_student'))
    
    return render_template('admin_add_student.html')


@app.route('/admin/students', methods=['GET'])
@admin_required
def admin_students():
    """Admin only: Manage all students"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query.filter_by(role='student')
    
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) | 
            (User.email.ilike(f'%{search}%'))
        )
    
    students_page = query.paginate(page=page, per_page=20)
    
    return render_template('admin_students.html', students=students_page, search=search)


@app.route('/admin/delete-student/<int:student_id>', methods=['POST'])
@admin_required
def admin_delete_student(student_id):
    """Admin only: Delete student"""
    student = User.query.get_or_404(student_id)
    
    if student.role != 'student':
        flash('Can only delete students', 'danger')
        return redirect(url_for('admin_students'))
    
    try:
        # Delete related records
        Attendance.query.filter_by(student_id=student_id).delete()
        Engagement.query.filter_by(student_id=student_id).delete()
        
        # Delete student
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {student.name} deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting student', 'danger')
    
    return redirect(url_for('admin_students'))


@app.route('/admin/teachers', methods=['GET'])
@admin_required
def admin_teachers():
    """Admin only: Manage all teachers"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query.filter_by(role='teacher')
    
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) | 
            (User.email.ilike(f'%{search}%'))
        )
    
    teachers_page = query.paginate(page=page, per_page=20)
    
    return render_template('admin_teachers.html', teachers=teachers_page, search=search)


@app.route('/admin/delete-teacher/<int:teacher_id>', methods=['POST'])
@admin_required
def admin_delete_teacher(teacher_id):
    """Admin only: Delete teacher"""
    
    teacher = User.query.get_or_404(teacher_id)
    
    if teacher.role != 'teacher':
        flash('Can only delete teachers', 'danger')
        return redirect(url_for('admin_teachers'))
    
    try:
        db.session.delete(teacher)
        db.session.commit()
        flash(f'Teacher {teacher.name} deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting teacher', 'danger')
    
    return redirect(url_for('admin_teachers'))


@app.route('/admin/bulk-add-students', methods=['GET', 'POST'])
@admin_required
def admin_bulk_add_students():
    """Admin only: Bulk add students (CSV)"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(url_for('admin_bulk_add_students'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('admin_bulk_add_students'))
        
        if not file.filename.endswith('.csv'):
            flash('Please upload a CSV file', 'danger')
            return redirect(url_for('admin_bulk_add_students'))
        
        try:
            stream = file.stream.read().decode('UTF8')
            import csv as csv_module
            reader = csv_module.DictReader(stream.split('\n'), fieldnames=['name', 'email', 'password'])
            
            added_count = 0
            skipped_count = 0
            
            for row in reader:
                if not row['name'] or not row['email'] or not row['password']:
                    skipped_count += 1
                    continue
                
                if User.query.filter_by(email=row['email']).first():
                    skipped_count += 1
                    continue
                
                student = User(name=row['name'], email=row['email'], role='student')
                student.set_password(row['password'])
                db.session.add(student)
                added_count += 1
            
            db.session.commit()
            flash(f'Added {added_count} students (Skipped: {skipped_count})', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error uploading file: {str(e)}', 'danger')
        
        return redirect(url_for('admin_bulk_add_students'))
    
    return render_template('admin_bulk_add_students.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Create tables and seed data
    with app.app_context():
        db.create_all()
        
        # Seed default subjects if not exist
        if Subject.query.count() == 0:
            subjects = [
                Subject(name='Mathematics'),
                Subject(name='Physics'),
                Subject(name='Chemistry'),
                Subject(name='English'),
                Subject(name='Programming'),
                Subject(name='Database Design')
            ]
            try:
                db.session.add_all(subjects)
                db.session.commit()
                print('[OK] Default subjects created')
            except:
                db.session.rollback()
        
        # Create demo faculty account if not exist
        if User.query.filter_by(email='faculty@example.com').first() is None:
            faculty = User(name='Prof. Smith', email='faculty@example.com', role='faculty')
            faculty.set_password('faculty123')
            try:
                db.session.add(faculty)
                db.session.commit()
                print('[OK] Demo faculty account created')
            except:
                db.session.rollback()
        
        # Create admin account if not exist
        if User.query.filter_by(email='admin@example.com').first() is None:
            admin = User(name='Administrator', email='admin@example.com', role='admin')
            admin.set_password('admin123')
            try:
                db.session.add(admin)
                db.session.commit()
                print('[OK] Admin account created')
            except:
                db.session.rollback()
        
        # Add 10 random teachers if count is below 10
        current_teacher_count = User.query.filter_by(role='teacher').count()
        if current_teacher_count < 10:
            teachers_needed = 10 - current_teacher_count
            print('[INFO] Generating %d random teachers...' % teachers_needed)
            
            new_teachers = generate_random_teachers(teachers_needed)
            
            try:
                db.session.add_all(new_teachers)
                db.session.commit()
                print('[OK] Successfully added %d teachers!' % len(new_teachers))
                print('   Total teachers now: %d' % User.query.filter_by(role="teacher").count())
            except Exception as e:
                db.session.rollback()
                print('[ERROR] Error adding teachers: %s' % str(e))
        
        # Add 50 random students if count is below 50
        current_student_count = User.query.filter_by(role='student').count()
        if current_student_count < 50:
            students_needed = 50 - current_student_count
            print('[INFO] Generating %d random students...' % students_needed)
            
            new_students = generate_random_students(students_needed)
            
            try:
                db.session.add_all(new_students)
                db.session.commit()
                print('[OK] Successfully added %d students!' % len(new_students))
                print('   Total students now: %d' % User.query.filter_by(role="student").count())
            except Exception as e:
                db.session.rollback()
                print('[ERROR] Error adding students: %s' % str(e))
        
        # Generate sample attendance and engagement data if not present
        attendance_count = Attendance.query.count()
        if attendance_count == 0:
            print('[INFO] Generating 6 months of sample attendance and engagement data...')
            generate_sample_attendance_engagement()
        
        print('\n' + '='*60)
        print('[INFO] APPLICATION STARTING...')
        print('='*60)
        print('Total Users: %d' % User.query.count())
        print('Total Students: %d' % User.query.filter_by(role="student").count())
        print('Total Faculty: %d' % User.query.filter_by(role="faculty").count())
        print('Total Subjects: %d' % Subject.query.count())
        print('Total Attendance Records: %d' % Attendance.query.count())
        print('Total Engagement Records: %d' % Engagement.query.count())
        print('='*60)
        print('\n[INFO] Open your browser and visit:')
        print('   http://127.0.0.1:5000\n')
        print('[INFO] Demo Login:')
        print('   Email:    faculty@example.com')
        print('   Password: faculty123\n')
        print('[INFO] All student passwords: student123\n')
        print('[INFO] Press CTRL+C to stop the server\n')
    
    app.run(debug=True, host='127.0.0.1', port=5000)
