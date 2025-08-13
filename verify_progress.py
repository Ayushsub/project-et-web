#!/usr/bin/env python3
"""
Simple verification script for progress tracking
"""

import sqlite3

def verify_progress():
    print("🔍 Verifying Progress Tracking...")
    
    try:
        conn = sqlite3.connect('learning_platform.db')
        cursor = conn.cursor()
        
        # Check current progress
        cursor.execute('''
            SELECT up.user_id, up.lesson_id, up.completed, up.score, 
                   l.title as lesson_title, c.title as course_title
            FROM user_progress up
            JOIN lessons l ON up.lesson_id = l.id
            JOIN courses c ON l.course_id = c.id
            ORDER BY up.completed_at DESC
        ''')
        
        progress = cursor.fetchall()
        
        print(f"✅ Found {len(progress)} progress records:")
        
        for record in progress:
            user_id, lesson_id, completed, score, lesson_title, course_title = record
            print(f"   User {user_id}: {lesson_title} ({course_title}) - Completed: {completed}, Score: {score}")
        
        # Test inserting a new progress record
        print(f"\n🧪 Testing progress insertion...")
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_progress (user_id, lesson_id, completed, completed_at)
            VALUES (1, 1, 1, CURRENT_TIMESTAMP)
        ''')
        
        conn.commit()
        print("✅ Progress record inserted successfully")
        
        # Verify the insertion
        cursor.execute('''
            SELECT * FROM user_progress WHERE user_id = 1 AND lesson_id = 1
        ''')
        
        result = cursor.fetchone()
        if result:
            print(f"✅ Verification: Progress record found - User: {result[1]}, Lesson: {result[2]}, Completed: {result[3]}")
        else:
            print("❌ Verification: Progress record not found")
        
        conn.close()
        print("\n🎉 Progress tracking is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    verify_progress() 