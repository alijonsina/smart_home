# 🏠 Smart Home Control System

A modern, user-friendly smart home control system built with Python and Tkinter. Control your lights, thermostats, and smart locks from a beautiful, intuitive interface.

## ✨ Features

### 🎨 Modern Interface
- **Clean, modern design** with a professional color scheme
- **Consistent styling** across all screens
- **Responsive layout** that adapts to different screen sizes
- **Intuitive navigation** with clear visual feedback

### 🔐 Authentication System
- **Secure login/signup** with user account management
- **Persistent user sessions** with automatic logout functionality
- **Consistent login experience** - same interface every time

### 🏠 Device Management
- **Multiple device types**: Lights, Thermostats, Smart Locks
- **Real-time control** with instant status updates
- **Device-specific controls**:
  - 💡 **Lights**: On/Off + Brightness control
  - 🌡️ **Thermostats**: Temperature + Mode (Heat/Cool/Off)
  - 🔒 **Smart Locks**: Lock/Unlock functionality
- **Add new devices** with an intuitive dialog
- **Persistent device storage** - your devices are saved between sessions

### 🎯 User Experience
- **Device cards** with clear status indicators
- **Color-coded status** (Green for ON/LOCKED, Red for OFF/UNLOCKED)
- **Scrollable interface** for managing many devices
- **Confirmation dialogs** for important actions
- **Error handling** with helpful messages

## 🚀 Quick Start

### Option 1: Command Line (Recommended)
```bash
# Navigate to the project directory
cd smart_home

# Run the launcher (handles environment issues)
python launch.py

# Or run directly
python main.py
```

### Option 2: Python Module
```python
from GUI.auth_gui import AuthGUI

app = AuthGUI()
app.run()
```

## 📁 Project Structure

```
smart_home/
├── GUI/
│   ├── auth_gui.py         # Authentication interface
│   ├── modern_home.py      # Modern home dashboard
│   └── home_page.py        # Legacy home page (backup)
├── Devices/
│   ├── device.py           # Device base classes
│   ├── device_manager.py   # Device management system
│   └── devices.json        # Device storage
├── User/
│   └── user_auth.py        # User authentication system
├── main.py                 # Main entry point
├── launch.py              # Environment-safe launcher
└── README.md              # This file
```

## 🎨 Interface Design

### Color Scheme
- **Primary Blue**: `#1976d2` - Main actions and highlights
- **Success Green**: `#059669` - ON status and positive actions
- **Danger Red**: `#dc2626` - OFF status and destructive actions
- **Background**: `#ffffff` - Clean white background
- **Surface**: `#f7f7f7` - Card backgrounds
- **Text**: `#222222` - Primary text color

### Typography
- **Font Family**: Segoe UI (Windows system font)
- **Headings**: Bold, larger sizes for hierarchy
- **Body Text**: Regular weight for readability
- **Status Text**: Bold for emphasis

## 🔧 Technical Details

### Dependencies
- **Python 3.6+** with tkinter (usually included)
- **No external packages** required - uses only standard library

### Architecture
- **Singleton Pattern**: DeviceManager ensures single instance
- **MVC Pattern**: Separation of data, logic, and presentation
- **Event-Driven**: Tkinter event system for user interactions
- **Persistent Storage**: JSON files for devices and user data

### Device Types
1. **Light**: On/Off status + brightness control (0-100%)
2. **Thermostat**: On/Off status + temperature (10-30°C) + mode
3. **Smart Lock**: Locked/Unlocked status

## 🎯 Usage Guide

### First Time Setup
1. Launch the application
2. Click "Don't have an account? Sign up"
3. Create your account with username and password
4. Sign in with your credentials
5. Your dashboard will show sample devices

### Managing Devices
1. **View Devices**: All your devices appear as cards on the dashboard
2. **Control Devices**: Use the ON/OFF buttons or device-specific controls
3. **Add Devices**: Click "➕ Add Device" and fill in the details
4. **Monitor Status**: Device status is shown in real-time with color coding

### Logging Out
- Click "🚪 Logout" in the top-right corner
- Confirm the logout action
- You'll return to the login screen

## 🐛 Troubleshooting

### Environment Issues
If you encounter `NameError: name 'bg_color' is not defined`:
1. Use `python launch.py` instead of `python main.py`
2. The launcher script bypasses environment issues
3. This is a known Python environment issue, not a code problem

### Missing Devices
- Devices are automatically loaded from `Devices/devices.json`
- If no devices appear, sample devices will be added automatically
- You can add new devices using the "Add Device" button

### GUI Issues
- Make sure tkinter is available: `python -c "import tkinter"`
- On Linux, you might need: `sudo apt-get install python3-tk`
- On macOS, tkinter should be included with Python

## 🔄 Recent Updates

### v2.1 - Device Loading Fix
- 🐛 Fixed device loading from JSON file
- 🔧 Proper status handling for all device types
- 🎯 Consistent device display in home screen
- 🔄 Improved logout functionality

### v2.0 - Modern Interface
- ✨ Complete UI redesign with modern styling
- 🎨 Consistent color scheme and typography
- 📱 Responsive layout improvements
- 🔄 Better logout functionality
- 🎯 Enhanced device management

### v1.0 - Initial Release
- 🔐 Basic authentication system
- 💡 Light device support
- 🌡️ Thermostat device support
- 🔒 Smart lock device support
- 💾 Persistent device storage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Enjoy controlling your smart home! 🏠✨**
