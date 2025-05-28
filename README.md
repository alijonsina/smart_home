# Smart Home Control System

A Python-based Smart Home Control System that demonstrates Object-Oriented Programming principles. This project implements a central control module for managing various smart home devices through a graphical user interface.

## Project Overview

The Smart Home Control System allows users to:
- Register and login securely
- Control various smart home devices (lights, thermostats, locks)
- Add and manage new devices
- Monitor device status in real-time
- Organize devices by location

## Features

### User Management
- Secure user registration and login
- Password hashing for security
- Persistent user data storage

### Device Management
- Support for multiple device types:
  - Smart Lights (brightness control)
  - Thermostats (temperature and mode control)
  - Smart Locks (lock/unlock functionality)
- Add new devices
- Remove existing devices
- Device status monitoring
- Location-based device organization

### User Interface
- Modern, responsive GUI using tkinter
- Intuitive device control panels
- Real-time status updates
- Easy navigation between devices
- Scrollable device list

## Technical Details

### Project Structure
```
smart_home/
├── Devices/           # Device management and device classes
│   ├── __init__.py
│   ├── device.py         # Device class hierarchy
│   ├── device_manager.py # Device management system
│   └── devices.json      # Device storage
├── GUI/              # User interface components
│   ├── __init__.py
│   ├── auth_gui.py      # Login/Registration interface
│   └── home_page.py     # Main dashboard
├── User/             # User authentication and management
│   ├── __init__.py
│   ├── user_auth.py     # User authentication system
│   └── users.json       # User storage
├── main.py           # Application entry point
└── requirements.txt  # Project dependencies
```

### Design Patterns Used

1. **Singleton Pattern**
   - DeviceManager ensures single instance throughout application
   - Centralized device management

2. **Factory Pattern**
   - DeviceManager acts as factory for creating devices
   - Flexible device creation system

3. **Observer Pattern**
   - GUI updates automatically with device state changes
   - Real-time status monitoring

4. **Abstract Factory**
   - Device abstract base class
   - Concrete implementations for different device types

### OOP Principles Demonstrated

1. **Encapsulation**
   - Private attributes in device classes
   - Property decorators for controlled access
   - Secure data handling

2. **Inheritance**
   - Device types inherit from base Device class
   - Common interface with specific implementations
   - Code reuse and organization

3. **Polymorphism**
   - Different device types implement common methods
   - Device-specific controls in GUI
   - Flexible device management

4. **Abstraction**
   - Abstract base class defining device interface
   - Separation of concerns
   - Clean architecture

## Installation

1. Ensure you have Python 3.7 or higher installed
2. Clone the repository:
   ```bash
   git clone [repository-url]
   cd smart_home
   ```
3. No external dependencies required (uses built-in tkinter)

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Register a new account or login with existing credentials

3. Use the dashboard to:
   - View all connected devices
   - Control device settings
   - Add new devices
   - Monitor device status

### Adding a New Device
1. Click "Add Device" in the dashboard
2. Select device type (Light, Thermostat, or Lock)
3. Enter device name and location
4. Click "Add Device" to confirm

### Controlling Devices
- **Lights**: 
  - Turn on/off
  - Adjust brightness (0-100%)
- **Thermostats**: 
  - Set temperature (10-30°C)
  - Choose mode (HEAT/COOL/OFF)
- **Locks**: 
  - Lock/Unlock doors
  - View lock status

## Security Features

1. **Password Security**
   - SHA-256 password hashing
   - Secure credential storage
   - Input validation

2. **Data Protection**
   - Secure file storage
   - User session management
   - Protected device access

## File Storage

1. `users.json`
   - Stores user credentials
   - Passwords are hashed
   - Created on first user registration

2. `devices.json`
   - Stores device configurations
   - Maintains device states
   - Created when first device is added

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Future Improvements

Potential areas for enhancement:
1. Add more device types
2. Implement device scheduling
3. Add automation rules
4. Implement user roles and permissions
5. Add device grouping
6. Implement device scenes
7. Add energy usage monitoring
8. Implement device notifications

## License

This project is open source and available under the MIT License.

## Author

[Your Name]

## Acknowledgments

- Python tkinter for GUI
- Python's built-in libraries for security and data management
