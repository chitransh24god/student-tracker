#!/usr/bin/env python3
"""
Student Attendance & Engagement Tracker - Universal Startup Script
This script handles everything: setup, installation, and running the app
Works on Windows, Linux, and Mac
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class AppLauncher:
    """Handle app launch, setup, and dependency installation"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.is_windows = platform.system() == "Windows"
        self.python_exe = self.get_python_executable()
        
    def get_python_executable(self):
        """Get Python executable path based on OS"""
        if self.is_windows:
            python_exe = self.venv_path / "Scripts" / "python.exe"
        else:
            python_exe = self.venv_path / "bin" / "python"
        
        if python_exe.exists():
            return str(python_exe)
        
        # Fallback to system Python
        return "python" if self.is_windows else "python3"
    
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║     🎓 STUDENT ATTENDANCE & ENGAGEMENT TRACKER                ║
║                                                                ║
║              Starting Application...                          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_venv(self):
        """Check if virtual environment exists"""
        if not self.venv_path.exists():
            print("\n📦 Virtual environment not found. Creating...")
            self.create_venv()
        else:
            print("\n✅ Virtual environment found!")
        
        # Update python executable path
        self.python_exe = self.get_python_executable()
    
    def create_venv(self):
        """Create virtual environment"""
        try:
            print("   Creating virtual environment...")
            subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_path)],
                check=True,
                capture_output=True
            )
            print("   ✅ Virtual environment created!")
        except Exception as e:
            print(f"   ❌ Error creating virtual environment: {e}")
            sys.exit(1)
    
    def install_dependencies(self):
        """Install required packages"""
        print("\n📚 Installing dependencies...")
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("   ❌ requirements.txt not found!")
            sys.exit(1)
        
        try:
            # Upgrade pip first
            print("   - Upgrading pip...")
            subprocess.run(
                [self.python_exe, "-m", "pip", "install", "--upgrade", "pip"],
                check=True,
                capture_output=True
            )
            print("   ✅ Pip upgraded!")
            
            # Install requirements
            print("   - Installing packages...")
            result = subprocess.run(
                [self.python_exe, "-m", "pip", "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("   ⚠️  Some packages failed to install:")
                print(result.stderr)
                print("\n   Attempting to install with compatible versions...")
                self.install_compatible_packages()
            else:
                print("   ✅ All packages installed successfully!")
                
        except Exception as e:
            print(f"   ❌ Error installing dependencies: {e}")
            sys.exit(1)
    
    def install_compatible_packages(self):
        """Install packages one by one with fallback versions"""
        packages = [
            "Flask==2.3.3",
            "Flask-SQLAlchemy==3.0.5",
            "Werkzeug==2.3.7",
            "python-dotenv==1.0.0"
        ]
        
        for package in packages:
            try:
                print(f"   - Installing {package}...")
                subprocess.run(
                    [self.python_exe, "-m", "pip", "install", package],
                    check=True,
                    capture_output=True
                )
                print(f"   ✅ {package} installed!")
            except:
                # Try without version
                pkg_name = package.split("==")[0]
                try:
                    print(f"   - Installing {pkg_name} (latest)...")
                    subprocess.run(
                        [self.python_exe, "-m", "pip", "install", pkg_name],
                        check=True,
                        capture_output=True
                    )
                    print(f"   ✅ {pkg_name} installed!")
                except Exception as e:
                    print(f"   ⚠️  Could not install {pkg_name}: {e}")
    
    def initialize_database(self):
        """Initialize database"""
        print("\n🗄️  Initializing database...")
        app_file = self.project_root / "app.py"
        
        if not app_file.exists():
            print("   ❌ app.py not found!")
            sys.exit(1)
        
        try:
            # Import Flask app and create tables
            init_code = f"""
import sys
sys.path.insert(0, r'{self.project_root}')
from app import app, db

with app.app_context():
    db.create_all()
    print('   ✅ Database initialized!')
"""
            result = subprocess.run(
                [self.python_exe, "-c", init_code],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"   ⚠️  Database initialization output:")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            else:
                print(result.stdout)
                
        except Exception as e:
            print(f"   ⚠️  Error initializing database: {e}")
    
    def run_app(self):
        """Run the Flask application"""
        print("\n" + "="*64)
        print("🚀 STARTING APPLICATION")
        print("="*64)
        print("\n📱 Application running at: http://127.0.0.1:5000")
        print("\n👤 Demo Credentials:")
        print("   Email:    faculty@example.com")
        print("   Password: faculty123")
        print("\n Press CTRL+C to stop the server")
        print("="*64 + "\n")
        
        try:
            app_file = self.project_root / "app.py"
            subprocess.run(
                [self.python_exe, str(app_file)],
                cwd=str(self.project_root)
            )
        except KeyboardInterrupt:
            print("\n\n👋 Application stopped. Goodbye!")
        except Exception as e:
            print(f"\n❌ Error running application: {e}")
            sys.exit(1)
    
    def launch(self):
        """Launch the application with full setup"""
        self.print_banner()
        
        # Check environment
        print("🔍 Checking environment...")
        print(f"   - OS: {platform.system()}")
        print(f"   - Python: {sys.version.split()[0]}")
        
        # Setup
        self.check_venv()
        self.install_dependencies()
        self.initialize_database()
        
        # Run
        self.run_app()


def main():
    """Main entry point"""
    try:
        launcher = AppLauncher()
        launcher.launch()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
