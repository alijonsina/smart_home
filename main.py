#!/usr/bin/env python3
"""
Smart Home Control System - Main Entry Point
"""

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from GUI.auth_gui import AuthGUI

def main():
    """Main entry point for the Smart Home Control System"""
    print("🏠 Starting Smart Home Control System...")
    
    # Start the authentication GUI
    app = AuthGUI()
    app.run()

if __name__ == "__main__":
    main() 