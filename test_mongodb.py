#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temple_attendance.settings')
django.setup()

from attendance.mongodb_utils import MongoDBManager

def test_mongodb_connection():
    """Test MongoDB connection and data retrieval"""
    print("Testing MongoDB connection...")
    
    # Test devotees collection
    devotees_db = MongoDBManager('devotees')
    devotee_count = devotees_db.count()
    print(f"Total devotees in database: {devotee_count}")
    
    if devotee_count > 0:
        # Get first few devotees
        devotees = devotees_db.find(limit=3)
        print("Sample devotees:")
        for devotee in devotees:
            print(f"  - {devotee.get('name', 'Unknown')} ({devotee.get('contact_number', 'No phone')})")
    
    # Test sabhas collection
    sabhas_db = MongoDBManager('sabhas')
    sabha_count = sabhas_db.count()
    print(f"Total sabhas in database: {sabha_count}")
    
    # Test attendance collection
    attendance_db = MongoDBManager('attendance_records')
    attendance_count = attendance_db.count()
    print(f"Total attendance records in database: {attendance_count}")
    
    print("MongoDB test completed.")

if __name__ == "__main__":
    test_mongodb_connection()