from typing import Dict, List, Optional, Type
from .device import Device, Light, Thermostat, SmartLock
import json
import os

class DeviceManager:
    """Singleton class to manage all smart home devices"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DeviceManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._devices: Dict[str, Device] = {}
        self._device_types: Dict[str, Type[Device]] = {
            "light": Light,
            "thermostat": Thermostat,
            "lock": SmartLock
        }
        self._devices_file = os.path.join(os.path.dirname(__file__), 'devices.json')
        self._load_devices()
        self._initialized = True

    def _load_devices(self):
        """Load devices from JSON file"""
        if os.path.exists(self._devices_file):
            try:
                with open(self._devices_file, 'r') as f:
                    devices_data = json.load(f)
                    for device_data in devices_data:
                        device_type = device_data.pop('type')
                        if device_type in self._device_types:
                            device_class = self._device_types[device_type]
                            device = device_class(**device_data)
                            self._devices[device.device_id] = device
            except Exception as e:
                print(f"Error loading devices: {e}")

    def _save_devices(self):
        """Save devices to JSON file"""
        devices_data = []
        for device in self._devices.values():
            device_dict = device.get_status_details()
            device_dict['type'] = device.__class__.__name__.lower()
            devices_data.append(device_dict)

        try:
            with open(self._devices_file, 'w') as f:
                json.dump(devices_data, f, indent=4)
        except Exception as e:
            print(f"Error saving devices: {e}")

    def add_device(self, device_type: str, device_id: str, name: str, location: str, **kwargs) -> Optional[Device]:
        """Add a new device"""
        if device_type not in self._device_types:
            return None

        if device_id in self._devices:
            return None

        device_class = self._device_types[device_type]
        device = device_class(device_id=device_id, name=name, location=location, **kwargs)
        self._devices[device_id] = device
        self._save_devices()
        return device

    def remove_device(self, device_id: str) -> bool:
        """Remove a device"""
        if device_id in self._devices:
            del self._devices[device_id]
            self._save_devices()
            return True
        return False

    def get_device(self, device_id: str) -> Optional[Device]:
        """Get a device by ID"""
        return self._devices.get(device_id)

    def get_all_devices(self) -> List[Device]:
        """Get all devices"""
        return list(self._devices.values())

    def get_devices_by_type(self, device_type: str) -> List[Device]:
        """Get all devices of a specific type"""
        if device_type not in self._device_types:
            return []
        return [device for device in self._devices.values() 
                if device.__class__.__name__.lower() == device_type]

    def get_devices_by_location(self, location: str) -> List[Device]:
        """Get all devices in a specific location"""
        return [device for device in self._devices.values() 
                if device.location.lower() == location.lower()] 