#!/usr/bin/env python
"""
Generate sample attendance and engagement data for past 6 months
This script populates the database with realistic test data for charting
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models import User, Subject, Attendance, Engagement
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate 6 months of attendance and engagement data"""
    
    with app.app_context():
        # Get all students and subjects
        students = User.query.filter_by(role='student').all()
        subjects = Subject.query.all()
        
        if not students:
            print('ERROR: No students found in database!')
            return
        
        if not subjects:
            print('ERROR: No subjects found in database!')
            return
        
        print('STARTING DATA GENERATION')
        print(f'  Students: {len(students)}')
        print(f'  Subjects: {len(subjects)}')
        print()
        
        # Clear existing records first
        print('CLEARING EXISTING DATA...')
        try:
            Attendance.query.delete()
            Engagement.query.delete()
            db.session.commit()
            print('  ✓ Old data cleared')
        except Exception as e:
            print(f'  Warning: Could not clear data: {e}')
            db.session.rollback()
        
        # Generate attendance data
        print('GENERATING ATTENDANCE DATA...')
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=180)  # 6 months ago
        
        # Generate data for each weekday
        current_date = start_date
        attendance_records = []
        days_processed = 0
        
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Monday=0 to Friday=4
                # For each subject
                for subject in subjects:
                    # For 70% of students
                    selected_students = random.sample(students, max(1, int(len(students) * 0.7)))
                    
                    for student in selected_students:
                        # 85% present, 15% absent
                        status = 'Present' if random.random() < 0.85 else 'Absent'
                        
                        attendance = Attendance(
                            student_id=student.id,
                            subject_id=subject.id,
                            date=current_date,
                            status=status
                        )
                        attendance_records.append(attendance)
            
            days_processed += 1
            if days_processed % 30 == 0:
                print(f'  Processed {days_processed} days (~{attendance_records.__len__()} records so far)...')
            
            current_date += timedelta(days=1)
        
        # Bulk insert attendance
        print(f'  Inserting {len(attendance_records)} attendance records...')
        for i, record in enumerate(attendance_records):
            db.session.add(record)
            if (i + 1) % 500 == 0:
                db.session.commit()
                print(f'    Committed {i + 1} records...')
        
        db.session.commit()
        print(f'✓ Created {len(attendance_records)} attendance records')
        print()
        
        # Generate engagement data
        print('GENERATING ENGAGEMENT DATA...')
        engagement_tags = [
            'Active Participation',
            'Late Submission',
            'Disruptive',
            'Excellent Work',
            'Improvement Needed',
            'Helps Peers',
            'Creative Thinking'
        ]
        
        engagement_records = []
        for student in students:
            # 15-30 engagements per student
            for _ in range(random.randint(15, 30)):
                random_date = start_date + timedelta(days=random.randint(0, 180))
                tag = random.choice(engagement_tags)
                note = 'Good performance in class'
                
                engagement = Engagement(
                    student_id=student.id,
                    subject_id=random.choice(subjects).id,
                    date=random_date,
                    tag=tag,
                    note=note
                )
                engagement_records.append(engagement)
        
        # Bulk insert engagement
        print(f'  Inserting {len(engagement_records)} engagement records...')
        for i, record in enumerate(engagement_records):
            db.session.add(record)
            if (i + 1) % 500 == 0:
                db.session.commit()
                print(f'    Committed {i + 1} records...')
        
        db.session.commit()
        print(f'✓ Created {len(engagement_records)} engagement records')
        print()
        
        # Final statistics
        print('=' * 60)
        print('DATA GENERATION COMPLETE!')
        print('=' * 60)
        attendance_total = Attendance.query.count()
        engagement_total = Engagement.query.count()
        print(f'Total Attendance Records: {attendance_total}')
        print(f'Total Engagement Records: {engagement_total}')
        print('=' * 60)

if __name__ == '__main__':
    generate_sample_data()
    print()
    print('Data generation script finished!')
    print('You can now start the app with: python app.py or START.bat')
