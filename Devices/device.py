from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

class Device(ABC):
    """Abstract base class for all smart home devices"""
    def __init__(self, device_id: str, name: str, location: str):
        self._device_id = device_id
        self._name = name
        self._location = location
        self._status = False  # False = off, True = on
        self._last_updated = datetime.now()

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def location(self) -> str:
        return self._location

    @property
    def status(self) -> bool:
        return self._status

    @property
    def last_updated(self) -> datetime:
        return self._last_updated

    @abstractmethod
    def turn_on(self) -> bool:
        """Turn on the device"""
        pass

    @abstractmethod
    def turn_off(self) -> bool:
        """Turn off the device"""
        pass

    @abstractmethod
    def get_status_details(self) -> Dict[str, Any]:
        """Get detailed status of the device"""
        pass

    def update_timestamp(self):
        """Update the last_updated timestamp"""
        self._last_updated = datetime.now()


class Light(Device):
    """Smart Light device"""
    def __init__(self, device_id: str, name: str, location: str, brightness: int = 100):
        super().__init__(device_id, name, location)
        self._brightness = min(max(brightness, 0), 100)  # Ensure brightness is between 0-100

    @property
    def brightness(self) -> int:
        return self._brightness

    def set_brightness(self, level: int) -> bool:
        """Set brightness level (0-100)"""
        if 0 <= level <= 100:
            self._brightness = level
            self.update_timestamp()
            return True
        return False

    def turn_on(self) -> bool:
        self._status = True
        self.update_timestamp()
        return True

    def turn_off(self) -> bool:
        self._status = False
        self.update_timestamp()
        return True

    def get_status_details(self) -> Dict[str, Any]:
        return {
            "device_id": self._device_id,
            "name": self._name,
            "location": self._location,
            "status": "ON" if self._status else "OFF",
            "brightness": self._brightness,
            "last_updated": self._last_updated.strftime("%Y-%m-%d %H:%M:%S")
        }


class Thermostat(Device):
    """Smart Thermostat device"""
    def __init__(self, device_id: str, name: str, location: str, temperature: float = 22.0):
        super().__init__(device_id, name, location)
        self._temperature = temperature
        self._mode = "HEAT"  # HEAT, COOL, or OFF

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def mode(self) -> str:
        return self._mode

    def set_temperature(self, temp: float) -> bool:
        """Set target temperature"""
        if 10 <= temp <= 30:  # Reasonable temperature range
            self._temperature = temp
            self.update_timestamp()
            return True
        return False

    def set_mode(self, mode: str) -> bool:
        """Set thermostat mode"""
        if mode in ["HEAT", "COOL", "OFF"]:
            self._mode = mode
            self.update_timestamp()
            return True
        return False

    def turn_on(self) -> bool:
        self._status = True
        self._mode = "HEAT"  # Default to heat mode when turning on
        self.update_timestamp()
        return True

    def turn_off(self) -> bool:
        self._status = False
        self._mode = "OFF"
        self.update_timestamp()
        return True

    def get_status_details(self) -> Dict[str, Any]:
        return {
            "device_id": self._device_id,
            "name": self._name,
            "location": self._location,
            "status": "ON" if self._status else "OFF",
            "temperature": self._temperature,
            "mode": self._mode,
            "last_updated": self._last_updated.strftime("%Y-%m-%d %H:%M:%S")
        }


class SmartLock(Device):
    """Smart Lock device"""
    def __init__(self, device_id: str, name: str, location: str):
        super().__init__(device_id, name, location)
        self._locked = True  # True = locked, False = unlocked

    @property
    def locked(self) -> bool:
        return self._locked

    def turn_on(self) -> bool:
        """Lock the door"""
        self._status = True
        self._locked = True
        self.update_timestamp()
        return True

    def turn_off(self) -> bool:
        """Unlock the door"""
        self._status = False
        self._locked = False
        self.update_timestamp()
        return True

    def get_status_details(self) -> Dict[str, Any]:
        return {
            "device_id": self._device_id,
            "name": self._name,
            "location": self._location,
            "status": "LOCKED" if self._locked else "UNLOCKED",
            "last_updated": self._last_updated.strftime("%Y-%m-%d %H:%M:%S")
        } 