#!/usr/bin/env python3
"""
Simple test for the learning platform
"""

import sqlite3

def test_basic():
    print("🔍 Basic Test...")
    
    try:
        conn = sqlite3.connect('learning_platform.db')
        cursor = conn.cursor()
        
        # Test users
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        print(f"Users: {user_count}")
        
        # Test courses
        cursor.execute('SELECT COUNT(*) FROM courses')
        course_count = cursor.fetchone()[0]
        print(f"Courses: {course_count}")
        
        # Test lessons
        cursor.execute('SELECT COUNT(*) FROM lessons')
        lesson_count = cursor.fetchone()[0]
        print(f"Lessons: {lesson_count}")
        
        # Test progress
        cursor.execute('SELECT COUNT(*) FROM user_progress')
        progress_count = cursor.fetchone()[0]
        print(f"Progress records: {progress_count}")
        
        conn.close()
        print("✅ Basic test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_basic() 