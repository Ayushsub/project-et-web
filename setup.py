#!/usr/bin/env python3
"""
Setup script for Learning Platform
This script helps install dependencies and set up the environment
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Error: Python 3.9 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_pip():
    """Install pip if not available"""
    try:
        import pip
        print("✅ pip is already installed")
        return True
    except ImportError:
        print("📦 Installing pip...")
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
            print("✅ pip installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install pip")
            return False

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["templates", "static", "static/css", "static/js", "static/images"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def check_dependencies():
    """Check if all dependencies are properly installed"""
    required_packages = [
        "flask",
        "flask_login", 
        "flask_wtf",
        "werkzeug",
        "python_dotenv",
        "gunicorn"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        return False
    return True

def main():
    """Main setup function"""
    print("🚀 Learning Platform Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install pip if needed
    if not install_pip():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Some dependencies are missing. Please run:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n✅ Setup completed successfully!")
    print("\n🎉 You can now run the application:")
    print("python app.py")
    print("\n🌐 Open your browser and go to: http://localhost:5000")

if __name__ == "__main__":
    main() 