import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine, text
from werkzeug.security import check_password_hash, generate_password_hash
import os

# Page config
st.set_page_config(page_title="Student Tracker", layout="wide", initial_sidebar_state="expanded")

# Initialize database
DB_PATH = "attendance.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

def init_db():
    """Initialize database connection"""
    with engine.connect() as conn:
        return conn

def get_user_by_email(email):
    """Get user by email"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})
        row = result.fetchone()
        if row:
            return dict(row._mapping) if row else None
    return None

def verify_password(stored_hash, password):
    """Verify password"""
    return check_password_hash(stored_hash, password)

# Custom CSS
st.markdown("""
<style>
    .main { padding: 1rem; }
    .stButton button { width: 100%; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

def login_page():
    """Login page"""
    st.title("📊 Student Attendance & Engagement Tracker")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Login")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Login As", ["Student", "Teacher", "Admin"])
        
        if st.button("Login", use_container_width=True):
            if email and password:
                user = get_user_by_email(email)
                
                if user:
                    role_map = {'Student': 'student', 'Teacher': 'teacher', 'Admin': 'admin'}
                    if user['role'] == role_map[role]:
                        if verify_password(user['password_hash'], password):
                            st.session_state.user_id = user['id']
                            st.session_state.user_email = user['email']
                            st.session_state.user_name = user['name']
                            st.session_state.user_role = user['role']
                            st.success(f"Welcome {user['name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid password")
                    else:
                        st.error(f"This account is a {user['role']}, not {role}")
                else:
                    st.error("Email not found")
            else:
                st.error("Please enter email and password")
        
        st.markdown("---")
        st.info("📝 Demo Credentials:\n- **Admin**: admin@example.com / Admin@123\n- **Teacher**: teacher1@example.com / Teacher@123\n- **Student**: student1@example.com / Student@123")

def dashboard_page():
    """Dashboard page"""
    st.title(f"📊 Dashboard - Welcome {st.session_state.user_name}")
    
    # Get user data
    with engine.connect() as conn:
        user_result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": st.session_state.user_id})
        user = dict(user_result.fetchone()._mapping)
    
    if user['role'] == 'student':
        # Student dashboard
        st.subheader("Your Attendance & Engagement Overview")
        
        with engine.connect() as conn:
            # Attendance stats
            att_result = conn.execute(text("""
                SELECT COUNT(*) as total, SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) as present
                FROM attendance WHERE student_id = :id
            """), {"id": st.session_state.user_id})
            att_data = dict(att_result.fetchone()._mapping)
            
            # Engagement stats
            eng_result = conn.execute(text("""
                SELECT COUNT(*) as total FROM engagement WHERE student_id = :id
            """), {"id": st.session_state.user_id})
            eng_data = dict(eng_result.fetchone()._mapping)
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_classes = att_data['total'] or 0
        attended = att_data['present'] or 0
        attendance_pct = (attended / total_classes * 100) if total_classes > 0 else 0
        
        with col1:
            st.metric("Total Classes", total_classes)
        with col2:
            st.metric("Classes Attended", attended)
        with col3:
            st.metric("Attendance %", f"{attendance_pct:.1f}%")
        with col4:
            st.metric("Engagement Records", eng_data['total'] or 0)
        
        # Charts
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly attendance trend
            with engine.connect() as conn:
                att_trend_result = conn.execute(text("""
                    SELECT DATE(date) as month, COUNT(*) as total, 
                           SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) as present
                    FROM attendance 
                    WHERE student_id = :id 
                    GROUP BY DATE(date)
                    ORDER BY DATE(date)
                    LIMIT 30
                """), {"id": st.session_state.user_id})
                trend_data = [dict(row._mapping) for row in att_trend_result.fetchall()]
            
            if trend_data:
                df_trend = pd.DataFrame(trend_data)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_trend['month'], y=df_trend['present'], mode='lines+markers', name='Present'))
                fig.update_layout(title="Attendance Trend (Last 30 days)", xaxis_title="Date", yaxis_title="Present")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top engagement tags
            with engine.connect() as conn:
                eng_tags_result = conn.execute(text("""
                    SELECT tag, COUNT(*) as count
                    FROM engagement 
                    WHERE student_id = :id 
                    GROUP BY tag
                    ORDER BY count DESC
                """), {"id": st.session_state.user_id})
                tags_data = [dict(row._mapping) for row in eng_tags_result.fetchall()]
            
            if tags_data:
                df_tags = pd.DataFrame(tags_data)
                fig = go.Figure(data=[go.Pie(labels=df_tags['tag'], values=df_tags['count'])])
                fig.update_layout(title="Engagement Distribution")
                st.plotly_chart(fig, use_container_width=True)
    
    elif user['role'] in ['teacher', 'admin']:
        # Teacher/Admin dashboard
        st.subheader("Dashboard Overview")
        
        with engine.connect() as conn:
            # Total stats
            students_result = conn.execute(text("SELECT COUNT(*) as count FROM users WHERE role='student'"))
            teachers_result = conn.execute(text("SELECT COUNT(*) as count FROM users WHERE role='teacher'"))
            att_result = conn.execute(text("SELECT COUNT(*) as count FROM attendance"))
            eng_result = conn.execute(text("SELECT COUNT(*) as count FROM engagement"))
            
            students_count = dict(students_result.fetchone()._mapping)['count']
            teachers_count = dict(teachers_result.fetchone()._mapping)['count']
            att_count = dict(att_result.fetchone()._mapping)['count']
            eng_count = dict(eng_result.fetchone()._mapping)['count']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", students_count)
        with col2:
            st.metric("Total Teachers", teachers_count)
        with col3:
            st.metric("Attendance Records", att_count)
        with col4:
            st.metric("Engagement Records", eng_count)

def attendance_page():
    """Add attendance"""
    st.title("📝 Add Attendance")
    
    with engine.connect() as conn:
        subjects_result = conn.execute(text("SELECT id, name FROM subjects"))
        subjects = [dict(row._mapping) for row in subjects_result.fetchall()]
        
        students_result = conn.execute(text("SELECT id, name FROM users WHERE role='student' ORDER BY name"))
        students = [dict(row._mapping) for row in students_result.fetchall()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_id = st.selectbox("Student", [{"id": s['id'], "name": s['name']} for s in students], 
                                   format_func=lambda x: x['name'])
    
    with col2:
        subject_id = st.selectbox("Subject", [(s['id'], s['name']) for s in subjects],
                                   format_func=lambda x: x[1])
    
    date = st.date_input("Date")
    status = st.radio("Status", ["Present", "Absent"])
    
    if st.button("Save Attendance", use_container_width=True):
        try:
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT OR REPLACE INTO attendance (student_id, subject_id, date, status)
                    VALUES (:student_id, :subject_id, :date, :status)
                """), {
                    "student_id": student_id['id'],
                    "subject_id": subject_id[0],
                    "date": date,
                    "status": status
                })
            st.success("✅ Attendance saved!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def engagement_page():
    """Add engagement"""
    st.title("💬 Add Engagement")
    
    with engine.connect() as conn:
        subjects_result = conn.execute(text("SELECT id, name FROM subjects"))
        subjects = [dict(row._mapping) for row in subjects_result.fetchall()]
        
        students_result = conn.execute(text("SELECT id, name FROM users WHERE role='student' ORDER BY name"))
        students = [dict(row._mapping) for row in students_result.fetchall()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_id = st.selectbox("Student", [{"id": s['id'], "name": s['name']} for s in students], 
                                   format_func=lambda x: x['name'], key="engagement_student")
    
    with col2:
        subject_id = st.selectbox("Subject", [(s['id'], s['name']) for s in subjects],
                                   format_func=lambda x: x[1], key="engagement_subject")
    
    date = st.date_input("Date", key="engagement_date")
    tag = st.selectbox("Tag", ["Active Participation", "Excellent Work", "Needs Improvement", "Absent", "Late Submission", "Others"])
    note = st.text_area("Note (optional)")
    
    if st.button("Save Engagement", use_container_width=True):
        try:
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO engagement (student_id, subject_id, date, tag, note)
                    VALUES (:student_id, :subject_id, :date, :tag, :note)
                """), {
                    "student_id": student_id['id'],
                    "subject_id": subject_id[0],
                    "date": date,
                    "tag": tag,
                    "note": note
                })
            st.success("✅ Engagement saved!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def students_page():
    """View and manage students"""
    st.title("👥 Students")
    
    search = st.text_input("Search students by name or email")
    
    with engine.connect() as conn:
        if search:
            query = text("""
                SELECT id, name, email, role, created_at FROM users 
                WHERE role='student' AND (name LIKE :search OR email LIKE :search)
                ORDER BY name
            """)
            result = conn.execute(query, {"search": f"%{search}%"})
        else:
            query = text("SELECT id, name, email, role, created_at FROM users WHERE role='student' ORDER BY name")
            result = conn.execute(query)
        
        students_data = [dict(row._mapping) for row in result.fetchall()]
    
    if students_data:
        df = pd.DataFrame(students_data)
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d')
        st.dataframe(df, use_container_width=True)
        
        # Expandable student details
        for student in students_data:
            with st.expander(f"📋 {student['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Email:** {student['email']}")
                    st.write(f"**Role:** {student['role']}")
                
                with col2:
                    st.write(f"**Joined:** {student['created_at']}")
                
                # View attendance
                with engine.connect() as conn:
                    att_result = conn.execute(text("""
                        SELECT a.*, s.name as subject_name FROM attendance a
                        JOIN subjects s ON a.subject_id = s.id
                        WHERE a.student_id = :id ORDER BY a.date DESC LIMIT 10
                    """), {"id": student['id']})
                    att_data = [dict(row._mapping) for row in att_result.fetchall()]
                
                if att_data:
                    st.write("**Recent Attendance:**")
                    for att in att_data:
                        status_emoji = "✅" if att['status'] == 'Present' else "❌"
                        st.caption(f"{status_emoji} {att['subject_name']} - {att['date']} ({att['status']})")
                
                # Delete student (admin only)
                if st.session_state.user_role == 'admin':
                    if st.button(f"🗑️ Delete {student['name']}", key=f"delete_{student['id']}"):
                        try:
                            with engine.begin() as conn:
                                conn.execute(text("DELETE FROM attendance WHERE student_id = :id"), {"id": student['id']})
                                conn.execute(text("DELETE FROM engagement WHERE student_id = :id"), {"id": student['id']})
                                conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": student['id']})
                            st.success(f"Deleted {student['name']}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
    else:
        st.info("No students found")

def settings_page():
    """Settings page"""
    st.title("⚙️ Settings")
    
    user_info = st.columns(2)
    
    with user_info[0]:
        st.subheader("👤 Profile Information")
        st.write(f"**Name:** {st.session_state.user_name}")
        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Role:** {st.session_state.user_role.title()}")
    
    with user_info[1]:
        st.subheader("🔐 Change Password")
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Update Password", use_container_width=True):
            if old_password and new_password and confirm_password:
                with engine.connect() as conn:
                    user_result = conn.execute(text("SELECT password_hash FROM users WHERE id = :id"), 
                                               {"id": st.session_state.user_id})
                    user = dict(user_result.fetchone()._mapping)
                
                if verify_password(user['password_hash'], old_password):
                    if new_password == confirm_password:
                        try:
                            with engine.begin() as conn:
                                hashed = generate_password_hash(new_password)
                                conn.execute(text("UPDATE users SET password_hash = :hash WHERE id = :id"), 
                                            {"hash": hashed, "id": st.session_state.user_id})
                            st.success("✅ Password updated!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.error("Passwords don't match")
                else:
                    st.error("Current password is incorrect")
            else:
                st.error("All fields are required")

def export_page():
    """Export data"""
    st.title("📤 Export Data")
    
    export_type = st.radio("Export Type", ["My Data", "All Students", "Attendance Report", "Engagement Report"])
    
    if export_type == "My Data" and st.session_state.user_role == 'student':
        with engine.connect() as conn:
            att_result = conn.execute(text("""
                SELECT a.*, s.name as subject_name FROM attendance a
                JOIN subjects s ON a.subject_id = s.id
                WHERE a.student_id = :id ORDER BY a.date DESC
            """), {"id": st.session_state.user_id})
            att_data = [dict(row._mapping) for row in att_result.fetchall()]
        
        if att_data:
            df = pd.DataFrame(att_data)
            csv = df.to_csv(index=False)
            st.download_button("Download Attendance CSV", csv, "attendance.csv", "text/csv")
    
    elif export_type == "All Students" and st.session_state.user_role == 'admin':
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, name, email, role, created_at FROM users WHERE role='student'"))
            data = [dict(row._mapping) for row in result.fetchall()]
        
        if data:
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            st.download_button("Download Students CSV", csv, "students.csv", "text/csv")
    
    elif st.session_state.user_role == 'admin':
        if export_type == "Attendance Report":
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT u.name as student, s.name as subject, a.date, a.status
                    FROM attendance a
                    JOIN users u ON a.student_id = u.id
                    JOIN subjects s ON a.subject_id = s.id
                    ORDER BY a.date DESC
                """))
                data = [dict(row._mapping) for row in result.fetchall()]
            
            if data:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button("Download Attendance Report", csv, "attendance_report.csv", "text/csv")
        
        elif export_type == "Engagement Report":
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT u.name as student, s.name as subject, e.date, e.tag, e.note
                    FROM engagement e
                    JOIN users u ON e.student_id = u.id
                    JOIN subjects s ON e.subject_id = s.id
                    ORDER BY e.date DESC
                """))
                data = [dict(row._mapping) for row in result.fetchall()]
            
            if data:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button("Download Engagement Report", csv, "engagement_report.csv", "text/csv")

def main():
    """Main app"""
    if 'user_id' not in st.session_state:
        login_page()
    else:
        # Sidebar navigation
        st.sidebar.title(f"👤 {st.session_state.user_name}")
        st.sidebar.subheader(f"Role: {st.session_state.user_role.title()}")
        st.sidebar.markdown("---")
        
        if st.session_state.user_role == 'student':
            page = st.sidebar.radio("Menu", ["Dashboard", "My Profile", "Export Data", "Settings", "Logout"])
        else:
            page = st.sidebar.radio("Menu", ["Dashboard", "➕ Attendance", "💬 Engagement", "👥 Students", "📤 Export", "⚙️ Settings", "Logout"])
        
        if page == "Dashboard":
            dashboard_page()
        elif page == "➕ Attendance":
            attendance_page()
        elif page == "💬 Engagement":
            engagement_page()
        elif page == "👥 Students":
            students_page()
        elif page == "My Profile":
            st.write(f"**Name:** {st.session_state.user_name}\n**Email:** {st.session_state.user_email}")
        elif page == "📤 Export" or page == "📤 Export Data":
            export_page()
        elif page == "⚙️ Settings":
            settings_page()
        elif page == "Logout":
            st.session_state.clear()
            st.success("Logged out successfully!")
            st.rerun()

if __name__ == "__main__":
    main()
