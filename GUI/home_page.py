import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from typing import Dict, Optional

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Devices.device_manager import DeviceManager
from Devices.device import Device, Light, Thermostat, SmartLock

class DeviceControlFrame(ttk.Frame):
    """Frame for controlling individual devices"""
    def __init__(self, parent, device: Device, **kwargs):
        super().__init__(parent, style="Custom.TFrame", padding="10", **kwargs)
        self.device = device
        self.create_widgets()

    def create_widgets(self):
        # Device name and location
        ttk.Label(self, text=f"{self.device.name}", style="DeviceName.TLabel").pack(anchor="w")
        ttk.Label(self, text=f"Location: {self.device.location}", style="Custom.TLabel").pack(anchor="w")
        
        # Status
        status_frame = ttk.Frame(self, style="Custom.TFrame")
        status_frame.pack(fill="x", pady=5)
        self.status_label = ttk.Label(status_frame, text=f"Status: {self.device.status}", 
                                    style="Status.TLabel")
        self.status_label.pack(side="left")
        
        # Control buttons
        btn_frame = ttk.Frame(self, style="Custom.TFrame")
        btn_frame.pack(fill="x", pady=5)
        
        self.on_btn = ttk.Button(btn_frame, text="ON", command=self.turn_on,
                               style="On.TButton")
        self.off_btn = ttk.Button(btn_frame, text="OFF", command=self.turn_off,
                                style="Off.TButton")
        self.on_btn.pack(side="left", padx=5)
        self.off_btn.pack(side="left", padx=5)

        # Device-specific controls
        if isinstance(self.device, Light):
            self.create_light_controls()
        elif isinstance(self.device, Thermostat):
            self.create_thermostat_controls()
        elif isinstance(self.device, SmartLock):
            self.create_lock_controls()

        self.update_status()

    def create_light_controls(self):
        """Create controls specific to Light devices"""
        control_frame = ttk.Frame(self, style="Custom.TFrame")
        control_frame.pack(fill="x", pady=5)
        
        ttk.Label(control_frame, text="Brightness:", style="Custom.TLabel").pack(side="left")
        self.brightness_scale = ttk.Scale(control_frame, from_=0, to=100, 
                                        orient="horizontal", length=150,
                                        command=self.update_brightness)
        self.brightness_scale.set(self.device.brightness)
        self.brightness_scale.pack(side="left", padx=5)

    def create_thermostat_controls(self):
        """Create controls specific to Thermostat devices"""
        control_frame = ttk.Frame(self, style="Custom.TFrame")
        control_frame.pack(fill="x", pady=5)
        
        # Temperature control
        temp_frame = ttk.Frame(control_frame, style="Custom.TFrame")
        temp_frame.pack(fill="x", pady=2)
        ttk.Label(temp_frame, text="Temperature:", style="Custom.TLabel").pack(side="left")
        self.temp_scale = ttk.Scale(temp_frame, from_=10, to=30, orient="horizontal",
                                  length=150, command=self.update_temperature)
        self.temp_scale.set(self.device.temperature)
        self.temp_scale.pack(side="left", padx=5)
        
        # Mode control
        mode_frame = ttk.Frame(control_frame, style="Custom.TFrame")
        mode_frame.pack(fill="x", pady=2)
        ttk.Label(mode_frame, text="Mode:", style="Custom.TLabel").pack(side="left")
        self.mode_var = tk.StringVar(value=self.device.mode)
        for mode in ["HEAT", "COOL", "OFF"]:
            ttk.Radiobutton(mode_frame, text=mode, value=mode, 
                           variable=self.mode_var,
                           command=self.update_mode).pack(side="left", padx=5)

    def create_lock_controls(self):
        """Create controls specific to SmartLock devices"""
        # Lock status is already handled by the main on/off buttons
        pass

    def update_brightness(self, value):
        """Update light brightness"""
        if isinstance(self.device, Light):
            self.device.set_brightness(int(float(value)))
            self.update_status()

    def update_temperature(self, value):
        """Update thermostat temperature"""
        if isinstance(self.device, Thermostat):
            self.device.set_temperature(float(value))
            self.update_status()

    def update_mode(self):
        """Update thermostat mode"""
        if isinstance(self.device, Thermostat):
            self.device.set_mode(self.mode_var.get())
            self.update_status()

    def turn_on(self):
        """Turn device on"""
        self.device.turn_on()
        self.update_status()

    def turn_off(self):
        """Turn device off"""
        self.device.turn_off()
        self.update_status()

    def update_status(self):
        """Update the status display"""
        status_text = "ON" if self.device.status else "OFF"
        if isinstance(self.device, SmartLock):
            status_text = "LOCKED" if self.device.locked else "UNLOCKED"
        self.status_label.config(text=f"Status: {status_text}")


class HomePage:
    def __init__(self, username: str):
        self.root = tk.Tk()
        self.root.title(f"Smart Home Control - {username}")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.device_manager = DeviceManager()
        self.setup_styles()
        self.create_widgets()
        
        # Add some sample devices if none exist
        if not self.device_manager.get_all_devices():
            self.add_sample_devices()

    def setup_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        style.configure("Custom.TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("DeviceName.TLabel", background="#f0f0f0", font=("Helvetica", 12, "bold"))
        style.configure("Status.TLabel", background="#f0f0f0", font=("Helvetica", 10, "italic"))
        style.configure("On.TButton", background="#4CAF50")
        style.configure("Off.TButton", background="#f44336")
        style.configure("Title.TLabel", background="#f0f0f0", font=("Helvetica", 16, "bold"))

    def create_widgets(self):
        """Create the main container and widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame", padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        title_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(title_frame, text="Smart Home Dashboard", 
                 style="Title.TLabel").pack(side="left")

        # Add device button
        ttk.Button(title_frame, text="Add Device", 
                  command=self.show_add_device_dialog).pack(side="right")

        # Devices container
        self.devices_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.devices_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable canvas for devices
        self.canvas = tk.Canvas(self.devices_frame, bg="#f0f0f0", 
                              highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.devices_frame, orient="vertical", 
                                     command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Custom.TFrame")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.refresh_devices()

    def refresh_devices(self):
        """Refresh the devices display"""
        # Clear existing devices
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Add device controls
        for device in self.device_manager.get_all_devices():
            device_frame = DeviceControlFrame(self.scrollable_frame, device)
            device_frame.pack(fill="x", pady=5, padx=5)
            ttk.Separator(self.scrollable_frame, orient="horizontal").pack(fill="x", pady=5)

    def show_add_device_dialog(self):
        """Show dialog to add a new device"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Device")
        dialog.geometry("300x400")
        dialog.configure(bg="#f0f0f0")
        dialog.transient(self.root)
        dialog.grab_set()

        # Device type selection
        ttk.Label(dialog, text="Device Type:", style="Custom.TLabel").pack(pady=5)
        device_type = tk.StringVar(value="light")
        for dtype in ["light", "thermostat", "lock"]:
            ttk.Radiobutton(dialog, text=dtype.capitalize(), value=dtype,
                           variable=device_type).pack()

        # Device details
        ttk.Label(dialog, text="Device Name:", style="Custom.TLabel").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack()

        ttk.Label(dialog, text="Location:", style="Custom.TLabel").pack(pady=5)
        location_entry = ttk.Entry(dialog, width=30)
        location_entry.pack()

        def add_device():
            name = name_entry.get().strip()
            location = location_entry.get().strip()
            dtype = device_type.get()

            if not name or not location:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            # Generate a simple device ID
            device_id = f"{dtype}_{name.lower().replace(' ', '_')}"
            
            if self.device_manager.add_device(dtype, device_id, name, location):
                self.refresh_devices()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to add device")

        ttk.Button(dialog, text="Add Device", command=add_device).pack(pady=20)

    def add_sample_devices(self):
        """Add some sample devices for demonstration"""
        sample_devices = [
            ("light", "living_room_light", "Living Room Light", "Living Room"),
            ("light", "bedroom_light", "Bedroom Light", "Bedroom"),
            ("thermostat", "main_thermostat", "Main Thermostat", "Living Room"),
            ("lock", "front_door", "Front Door Lock", "Entrance")
        ]

        for dtype, device_id, name, location in sample_devices:
            self.device_manager.add_device(dtype, device_id, name, location)
        self.refresh_devices()

    def run(self):
        """Start the application"""
        self.root.mainloop() 