import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from GUI.auth_gui import AuthGUI

def main():
    """Main entry point for the smart home application"""
    app = AuthGUI()
    app.run()

if __name__ == "__main__":
    main() 