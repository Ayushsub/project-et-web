# Learning Platform for Young Students

A fun and interactive learning website designed specifically for students under 8th grade. The platform offers courses in Math, Science, English, and Computer Basics with interactive content including text lessons, videos, and quizzes.

## Features

- 🎓 **User Registration & Login**: Simple registration and login system
- 📚 **Interactive Courses**: Math, Science, English, and Computer Basics
- 🎥 **Video Lessons**: Embedded educational videos
- ❓ **Interactive Quizzes**: Fun quizzes with immediate feedback
- 📊 **Progress Tracking**: Monitor learning progress
- 📈 **Clickstream Analytics**: Track all user interactions
- 🎨 **Child-Friendly Design**: Colorful, engaging interface
- 📱 **Responsive Design**: Works on all devices

## Clickstream Data Tracking

The platform tracks all user interactions and stores them in a CSV file (`clickstream_data.csv`) with the following format:

| Time | Event context | Component | Event name | Description | Origin | IP address |
|------|---------------|-----------|------------|-------------|---------|------------|
| 5/08/24, 02:57:25 | Course: Math Basics | Lesson | Lesson viewed | User viewed lesson | web | 10.167.9.55 |

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (local) / PostgreSQL (production)
- **Authentication**: Flask-Login
- **Deployment**: Render/Vercel/Heroku ready

## Installation & Setup

### Prerequisites

1. **Python 3.9+**: Download from [python.org](https://python.org)
2. **Git**: Download from [git-scm.com](https://git-scm.com)

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd learning-platform
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
learning-platform/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── runtime.txt           # Python version specification
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── course.html       # Course page
│   └── lesson.html       # Lesson page
├── static/               # Static files (CSS, JS, images)
└── learning_platform.db  # SQLite database (created automatically)
```

## Sample Data

The application comes with pre-loaded sample courses:

1. **Basic Math for Kids**: Addition, subtraction, multiplication, division
2. **Science Adventures**: Interactive science experiments
3. **English Grammar**: Parts of speech, grammar rules
4. **Computer Basics**: Computer fundamentals and usage


## Usage

1. **Register**: Create a new account with username, email, and password
2. **Login**: Access your personalized dashboard
3. **Browse Courses**: Choose from available courses
4. **Take Lessons**: Complete text, video, and quiz lessons
5. **Track Progress**: Monitor your learning journey
6. **Review**: Revisit completed lessons anytime

## Clickstream Analytics

All user interactions are automatically logged to `clickstream_data.csv`:

- Page views
- Course access
- Lesson completions
- Quiz attempts and scores
- Login/logout events
- User registration

## Customization


## Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection
- Input validation
- Secure headers

## Performance Optimization

- Static file caching
- Database indexing
- Efficient queries
- Responsive design
