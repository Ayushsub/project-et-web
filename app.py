from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import csv
import os
from datetime import datetime
import json

# Add custom Jinja2 filter for JSON parsing
def from_json_filter(value):
    if value:
        return json.loads(value)
    return None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Register the custom filter
app.jinja_env.filters['from_json'] = from_json_filter

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database setup
def init_db():
    conn = sqlite3.connect('learning_platform.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            difficulty TEXT DEFAULT 'Beginner',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Lessons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            title TEXT NOT NULL,
            content TEXT,
            lesson_type TEXT DEFAULT 'text',
            video_url TEXT,
            quiz_data TEXT,
            order_num INTEGER,
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')
    
    # User progress table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lesson_id INTEGER,
            completed BOOLEAN DEFAULT FALSE,
            score INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Clickstream tracking
def log_clickstream(event_context, component, event_name, description, origin="web"):
    timestamp = datetime.now().strftime("%m/%d/%y, %H:%M:%S")
    user_id = current_user.id if current_user.is_authenticated else "anonymous"
    ip_address = request.remote_addr
    
    # Create CSV file if it doesn't exist
    csv_file = 'clickstream_data.csv'
    file_exists = os.path.exists(csv_file)
    
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header if file is new
        if not file_exists:
            writer.writerow(['Time', 'Event context', 'Component', 'Event name', 'Description', 'Origin', 'IP address'])
        
        writer.writerow([timestamp, event_context, component, event_name, description, origin, ip_address])

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('learning_platform.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

# Routes
@app.route('/')
def index():
    log_clickstream("Homepage", "System", "Page viewed", "User visited the homepage")
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('learning_platform.db')
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            flash('Username or email already exists!')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', 
                      (username, email, password_hash))
        conn.commit()
        conn.close()
        
        log_clickstream("Registration", "System", "User registered", f"New user '{username}' registered")
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('learning_platform.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, password_hash FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            log_clickstream("Login", "System", "User logged in", f"User '{username}' logged in")
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    log_clickstream("Logout", "System", "User logged out", f"User '{current_user.username}' logged out")
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect('learning_platform.db')
    cursor = conn.cursor()
    
    # Get all courses
    cursor.execute('SELECT * FROM courses ORDER BY created_at DESC')
    courses = cursor.fetchall()
    
    # Get user progress
    cursor.execute('''
        SELECT c.id, c.title, COUNT(up.id) as completed_lessons, 
               (SELECT COUNT(*) FROM lessons WHERE course_id = c.id) as total_lessons
        FROM courses c
        LEFT JOIN lessons l ON c.id = l.course_id
        LEFT JOIN user_progress up ON l.id = up.lesson_id AND up.user_id = ? AND up.completed = 1
        GROUP BY c.id, c.title
    ''', (current_user.id,))
    progress = cursor.fetchall()
    
    conn.close()
    
    log_clickstream("Dashboard", "System", "Dashboard viewed", f"User '{current_user.username}' viewed dashboard")
    return render_template('dashboard.html', courses=courses, progress=progress)

@app.route('/course/<int:course_id>')
@login_required
def course(course_id):
    conn = sqlite3.connect('learning_platform.db')
    cursor = conn.cursor()
    
    # Get course details
    cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
    course_data = cursor.fetchone()
    
    if not course_data:
        conn.close()
        flash('Course not found!')
        return redirect(url_for('dashboard'))
    
    # Get lessons
    cursor.execute('SELECT * FROM lessons WHERE course_id = ? ORDER BY order_num', (course_id,))
    lessons = cursor.fetchall()
    
    # Get user progress for this course
    cursor.execute('''
        SELECT l.id, up.completed, up.score
        FROM lessons l
        LEFT JOIN user_progress up ON l.id = up.lesson_id AND up.user_id = ?
        WHERE l.course_id = ?
        ORDER BY l.order_num
    ''', (current_user.id, course_id))
    progress = cursor.fetchall()
    
    conn.close()
    
    log_clickstream(f"Course: {course_data[1]}", "System", "Course viewed", 
                   f"User '{current_user.username}' viewed course '{course_data[1]}'")
    
    return render_template('course.html', course=course_data, lessons=lessons, progress=progress)

@app.route('/lesson/<int:lesson_id>')
@login_required
def lesson(lesson_id):
    conn = sqlite3.connect('learning_platform.db')
    cursor = conn.cursor()
    
    # Get lesson details
    cursor.execute('''
        SELECT l.*, c.title as course_title 
        FROM lessons l 
        JOIN courses c ON l.course_id = c.id 
        WHERE l.id = ?
    ''', (lesson_id,))
    lesson_data = cursor.fetchone()
    
    if not lesson_data:
        conn.close()
        flash('Lesson not found!')
        return redirect(url_for('dashboard'))
    
    # Get user progress for this lesson
    cursor.execute('SELECT * FROM user_progress WHERE user_id = ? AND lesson_id = ?', 
                  (current_user.id, lesson_id))
    progress = cursor.fetchone()
    
    conn.close()
    
    log_clickstream(f"Course: {lesson_data[7]}", "Lesson", "Lesson viewed", 
                   f"User '{current_user.username}' viewed lesson '{lesson_data[2]}'")
    
    return render_template('lesson.html', lesson=lesson_data, progress=progress)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    data = request.get_json()
    lesson_id = data.get('lesson_id')
    answers = data.get('answers')
    score = data.get('score')
    
    conn = sqlite3.connect('learning_platform.db')
    cursor = conn.cursor()
    
    # Update or insert progress
    cursor.execute('''
        INSERT OR REPLACE INTO user_progress (user_id, lesson_id, completed, score, completed_at)
        VALUES (?, ?, 1, ?, CURRENT_TIMESTAMP)
    ''', (current_user.id, lesson_id, score))
    
    conn.commit()
    conn.close()
    
    log_clickstream("Quiz", "Quiz", "Quiz completed", 
                   f"User '{current_user.username}' completed quiz with score {score}")
    
    return jsonify({'success': True, 'score': score})

# @app.route('/mark_complete', methods=['POST'])
# @login_required
# def mark_complete():
#     data = request.get_json()
#     lesson_id = data.get('lesson_id')
    
#     conn = sqlite3.connect('learning_platform.db')
#     cursor = conn.cursor()
    
#     # Update or insert progress
#     cursor.execute('''
#         INSERT OR REPLACE INTO user_progress (user_id, lesson_id, completed, completed_at)
#         VALUES (?, ?, 1, CURRENT_TIMESTAMP)
#     ''', (current_user.id, lesson_id))
    
#     conn.commit()
#     conn.close()
    
#     log_clickstream("Lesson", "Lesson", "Lesson completed", 
#                    f"User '{current_user.username}' marked lesson as complete")
    
#     return jsonify({'success': True})

@app.route('/mark_complete', methods=['POST'])
@login_required
def mark_complete():
    data = request.get_json()
    lesson_id = data.get('lesson_id')

    if not lesson_id:
        return jsonify({'success': False, 'error': 'No lesson ID provided'}), 400

    conn = sqlite3.connect('learning_platform.db')
    cursor = conn.cursor()

    # Check if progress already exists
    cursor.execute('''
        SELECT completed FROM user_progress
        WHERE user_id = ? AND lesson_id = ?
    ''', (current_user.id, lesson_id))
    existing = cursor.fetchone()

    if existing:
        # Update existing record
        cursor.execute('''
            UPDATE user_progress
            SET completed = 1,
                completed_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND lesson_id = ?
        ''', (current_user.id, lesson_id))
    else:
        # Insert new progress record
        cursor.execute('''
            INSERT INTO user_progress (user_id, lesson_id, completed, completed_at)
            VALUES (?, ?, 1, CURRENT_TIMESTAMP)
        ''', (current_user.id, lesson_id))

    conn.commit()
    conn.close()

    log_clickstream(
        "Lesson", 
        "Lesson", 
        "Lesson completed", 
        f"User '{current_user.username}' marked lesson as complete"
    )

    return jsonify({'success': True})


# Sample data insertion
def insert_sample_data():
    conn = sqlite3.connect('learning_platform.db')
    cursor = conn.cursor()
    
    # Check if sample data already exists
    cursor.execute('SELECT COUNT(*) FROM courses')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Insert sample courses
    courses = [
        ('Basic Math for Kids', 'Learn addition, subtraction, multiplication, and division in a fun way!', 'Beginner'),
        ('Science Adventures', 'Explore the wonders of science through interactive experiments', 'Beginner'),
        ('English Grammar', 'Master English grammar with simple explanations and exercises', 'Beginner'),
        ('Computer Basics', 'Learn how to use computers and basic software', 'Beginner')
    ]
    
    for course in courses:
        cursor.execute('INSERT INTO courses (title, description, difficulty) VALUES (?, ?, ?)', course)
    
    # Get course IDs
    cursor.execute('SELECT id FROM courses')
    course_ids = [row[0] for row in cursor.fetchall()]
    
    # Insert sample lessons
    lessons = [
        # Math course lessons
        (course_ids[0], 'Addition Basics', 'Learn how to add numbers together!', 'text', '', '', 1),
        (course_ids[0], 'Addition Quiz', '', 'quiz', '', json.dumps({
            'questions': [
                {'question': 'What is 5 + 3?', 'options': ['6', '7', '8', '9'], 'correct': 2},
                {'question': 'What is 10 + 7?', 'options': ['15', '16', '17', '18'], 'correct': 2},
                {'question': 'What is 2 + 8?', 'options': ['8', '9', '10', '11'], 'correct': 2}
            ]
        }), 2),
        (course_ids[0], 'Subtraction Video', 'Watch this fun video about subtraction!', 'video', 'https://www.youtube.com/embed/dQw4w9WgXcQ', '', 3),
        
        # Science course lessons
        (course_ids[1], 'What is Science?', 'Science is all around us! Let\'s learn what it means.', 'text', '', '', 1),
        (course_ids[1], 'Simple Experiments', 'Try these safe experiments at home!', 'text', '', '', 2),
        (course_ids[1], 'Science Quiz', '', 'quiz', '', json.dumps({
            'questions': [
                {'question': 'What do plants need to grow?', 'options': ['Water', 'Sunlight', 'Both', 'Neither'], 'correct': 2},
                {'question': 'What is the closest planet to the Sun?', 'options': ['Earth', 'Mars', 'Mercury', 'Venus'], 'correct': 2}
            ]
        }), 3),
        
        # English course lessons
        (course_ids[2], 'Parts of Speech', 'Learn about nouns, verbs, and adjectives!', 'text', '', '', 1),
        (course_ids[2], 'Grammar Quiz', '', 'quiz', '', json.dumps({
            'questions': [
                {'question': 'Which word is a noun?', 'options': ['Run', 'Fast', 'Dog', 'Quickly'], 'correct': 2},
                {'question': 'Which word is a verb?', 'options': ['Happy', 'Jump', 'Big', 'Red'], 'correct': 1}
            ]
        }), 2),
        
        # Computer course lessons
        (course_ids[3], 'What is a Computer?', 'Learn about different types of computers!', 'text', '', '', 1),
        (course_ids[3], 'Using a Mouse', 'Practice using your computer mouse!', 'text', '', '', 2),
        (course_ids[3], 'Computer Quiz', '', 'quiz', '', json.dumps({
            'questions': [
                {'question': 'What do you use to click on things?', 'options': ['Keyboard', 'Mouse', 'Monitor', 'Speaker'], 'correct': 1},
                {'question': 'What shows you what\'s on the computer?', 'options': ['Mouse', 'Keyboard', 'Monitor', 'Printer'], 'correct': 2}
            ]
        }), 3)
    ]
    
    for lesson in lessons:
        cursor.execute('''
            INSERT INTO lessons (course_id, title, content, lesson_type, video_url, quiz_data, order_num)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', lesson)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    insert_sample_data()
    app.run(debug=True) 