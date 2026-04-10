#!/usr/bin/env python
"""Test the API endpoints"""

import sys
sys.path.insert(0, '.')

from app import app, db
from models import User, Subject, Attendance, Engagement
from datetime import datetime, timedelta
from sqlalchemy import func, case

def test_attendance_by_subject():
    """Test attendance by subject query"""
    with app.app_context():
        print("Testing attendance by subject query...")
        
        try:
            query = db.session.query(
                Subject.name,
                func.sum(case((Attendance.status == 'Present', 1), else_=0)).label('present'),
                func.count(Attendance.id).label('total')
            ).join(Attendance, Subject.id == Attendance.subject_id).group_by(Subject.id, Subject.name)
            
            results = query.all()
            print(f"✓ Found {len(results)} subjects with attendance data")
            for subject, present, total in results[:3]:
                pct = round((present or 0) / total * 100) if total > 0 else 0
                print(f"  - {subject}: {present}/{total} ({pct}%)")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()

def test_monthly_trend():
    """Test monthly trend query"""
    with app.app_context():
        print("\nTesting monthly trend query...")
        
        try:
            six_months_ago = datetime.now().date() - timedelta(days=180)
            
            query = db.session.query(
                func.strftime('%Y-%m', Attendance.date).label('month'),
                func.sum(case((Attendance.status == 'Present', 1), else_=0)).label('present'),
                func.count(Attendance.id).label('total')
            ).filter(Attendance.date >= six_months_ago).group_by(
                func.strftime('%Y-%m', Attendance.date)
            )
            
            results = query.order_by('month').all()
            print(f"✓ Found {len(results)} months of data")
            for month, present, total in results[:3]:
                pct = round((present or 0) / total * 100) if total > 0 else 0
                print(f"  - {month}: {present}/{total} ({pct}%)")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()

def test_engagement_distribution():
    """Test engagement distribution query"""
    with app.app_context():
        print("\nTesting engagement distribution query...")
        
        try:
            query = db.session.query(
                Engagement.tag,
                func.count(Engagement.id).label('count')
            ).group_by(Engagement.tag)
            
            results = query.all()
            print(f"✓ Found {len(results)} engagement tags")
            for tag, count in results:
                print(f"  - {tag}: {count} records")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_attendance_by_subject()
    test_monthly_trend()
    test_engagement_distribution()
    print("\n✓ All tests completed!")
