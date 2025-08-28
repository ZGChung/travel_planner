#!/usr/bin/env python3
"""
智能旅游酒店推荐系统启动脚本
Simple startup script for the Travel Planner application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import requests
        import pandas
        import numpy
        print("✅ All dependencies are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main function to start the application."""
    print("🏨 智能旅游酒店推荐系统")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("🚀 Starting the application...")
    print("📱 The app will open in your default browser")
    print("🔗 If it doesn't open automatically, visit: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped. Thank you for using the Travel Planner!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()