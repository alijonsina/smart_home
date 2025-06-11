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
        super().__init__(parent, style="DeviceCard.TFrame", padding="15", **kwargs)
        self.device = device
        self.create_widgets()

    def create_widgets(self):
        # Device header with name and location
        header_frame = ttk.Frame(self, style="DeviceCard.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text=f"{self.device.name}", 
                 style="DeviceName.TLabel").pack(side="left")
        ttk.Label(header_frame, text=f"📍 {self.device.location}", 
                 style="Location.TLabel").pack(side="right")
        
        # Status with modern styling
        status_frame = ttk.Frame(self, style="DeviceCard.TFrame")
        status_frame.pack(fill="x", pady=(0, 15))
        
        status_text = "ON" if self.device.status else "OFF"
        if isinstance(self.device, SmartLock):
            status_text = "LOCKED" if self.device.locked else "UNLOCKED"
        
        status_style = "StatusOn.TLabel" if (self.device.status or 
                                           (isinstance(self.device, SmartLock) and self.device.locked)) else "StatusOff.TLabel"
        self.status_label = ttk.Label(status_frame, text=f"Status: {status_text}", 
                                    style=status_style)
        self.status_label.pack(side="left")
        
        # Control buttons with modern styling
        btn_frame = ttk.Frame(self, style="DeviceCard.TFrame")
        btn_frame.pack(fill="x", pady=(0, 10))
        
        self.on_btn = ttk.Button(btn_frame, text="🔆 ON", command=self.turn_on,
                               style="On.TButton")
        self.off_btn = ttk.Button(btn_frame, text="⭕ OFF", command=self.turn_off,
                                style="Off.TButton")
        self.on_btn.pack(side="left", padx=(0, 10))
        self.off_btn.pack(side="left")

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
        control_frame = ttk.Frame(self, style="DeviceCard.TFrame")
        control_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(control_frame, text="💡 Brightness:", style="ControlLabel.TLabel").pack(side="left")
        self.brightness_scale = ttk.Scale(control_frame, from_=0, to=100, 
                                        orient="horizontal", length=200,
                                        command=self.update_brightness)
        self.brightness_scale.set(self.device.brightness)
        self.brightness_scale.pack(side="left", padx=10)

    def create_thermostat_controls(self):
        """Create controls specific to Thermostat devices"""
        control_frame = ttk.Frame(self, style="DeviceCard.TFrame")
        control_frame.pack(fill="x", pady=(10, 0))
        
        # Temperature control
        temp_frame = ttk.Frame(control_frame, style="DeviceCard.TFrame")
        temp_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(temp_frame, text="🌡️ Temperature:", style="ControlLabel.TLabel").pack(side="left")
        self.temp_scale = ttk.Scale(temp_frame, from_=10, to=30, orient="horizontal",
                                  length=200, command=self.update_temperature)
        self.temp_scale.set(self.device.temperature)
        self.temp_scale.pack(side="left", padx=10)
        
        # Mode control
        mode_frame = ttk.Frame(control_frame, style="DeviceCard.TFrame")
        mode_frame.pack(fill="x")
        ttk.Label(mode_frame, text="Mode:", style="ControlLabel.TLabel").pack(side="left")
        self.mode_var = tk.StringVar(value=self.device.mode)
        for mode in ["HEAT", "COOL", "OFF"]:
            ttk.Radiobutton(mode_frame, text=mode, value=mode, 
                           variable=self.mode_var,
                           command=self.update_mode,
                           style="Mode.TRadiobutton").pack(side="left", padx=(10, 5))

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
        
        status_style = "StatusOn.TLabel" if (self.device.status or 
                                           (isinstance(self.device, SmartLock) and self.device.locked)) else "StatusOff.TLabel"
        self.status_label.config(text=f"Status: {status_text}", style=status_style)


class HomePage:
    def __init__(self, username: str):
        self.bg_color = "#ffffff"
        self.card_bg = "#f7f7f7"
        self.text_color = "#222222"
        self.accent_color = "#1976d2"
        self.danger_color = "#f44336"
        
        self.root = tk.Tk()
        self.root.title(f"Smart Home Control - {username}")
        self.root.geometry("900x700")
        self.root.configure(bg=self.bg_color)
        
        # Store username for logout functionality
        self.username = username
        
        self.device_manager = DeviceManager()
        self.setup_styles()
        self.create_widgets()
        
        # Add some sample devices if none exist
        if not self.device_manager.get_all_devices():
            self.add_sample_devices()

    def setup_styles(self):
        """Configure modern styles for widgets"""
        style = ttk.Style()
        
        # Frame styles
        style.configure("Custom.TFrame", background=self.bg_color)
        style.configure("DeviceCard.TFrame", background=self.card_bg, relief="raised", borderwidth=1)
        
        # Label styles
        style.configure("Custom.TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 20, "bold"))
        style.configure("DeviceName.TLabel", background=self.card_bg, foreground=self.text_color, font=("Segoe UI", 14, "bold"))
        style.configure("Location.TLabel", background=self.card_bg, foreground="#888888", font=("Segoe UI", 10))
        style.configure("StatusOn.TLabel", background=self.card_bg, foreground=self.accent_color, font=("Segoe UI", 10, "bold"))
        style.configure("StatusOff.TLabel", background=self.card_bg, foreground="#888888", font=("Segoe UI", 10))
        style.configure("ControlLabel.TLabel", background=self.card_bg, foreground=self.text_color, font=("Segoe UI", 10))
        
        # Button styles
        style.configure("On.TButton", background=self.accent_color, foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("Off.TButton", background=self.danger_color, foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("Logout.TButton", background="#666666", foreground="white", font=("Segoe UI", 10))
        style.configure("AddDevice.TButton", background=self.accent_color, foreground="white", font=("Segoe UI", 10, "bold"))
        
        # Radio button style
        style.configure("Mode.TRadiobutton", background=self.card_bg, foreground=self.text_color, font=("Segoe UI", 9))

    def create_widgets(self):
        """Create the main container and widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame", padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header with title, user info, and logout
        header_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Left side - title
        title_frame = ttk.Frame(header_frame, style="Custom.TFrame")
        title_frame.pack(side="left")
        ttk.Label(title_frame, text="🏠 Smart Home Dashboard", 
                 style="Title.TLabel").pack(anchor="w")
        ttk.Label(title_frame, text=f"Welcome back, {self.username}!", 
                 style="Custom.TLabel").pack(anchor="w")
        
        # Right side - buttons
        button_frame = ttk.Frame(header_frame, style="Custom.TFrame")
        button_frame.pack(side="right")
        
        ttk.Button(button_frame, text="➕ Add Device", 
                  command=self.show_add_device_dialog,
                  style="AddDevice.TButton").pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="🚪 Logout", 
                  command=self.logout,
                  style="Logout.TButton").pack(side="left")

        # Devices container
        self.devices_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.devices_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable canvas for devices
        self.canvas = tk.Canvas(self.devices_frame, bg=self.bg_color, 
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

    def logout(self):
        """Handle logout functionality"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            # Reopen the auth GUI
            from GUI.auth_gui import AuthGUI
            auth_app = AuthGUI()
            auth_app.run()

    def refresh_devices(self):
        """Refresh the devices display"""
        # Clear existing devices
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Add device controls
        for device in self.device_manager.get_all_devices():
            device_frame = DeviceControlFrame(self.scrollable_frame, device)
            device_frame.pack(fill="x", pady=10, padx=5)
            ttk.Separator(self.scrollable_frame, orient="horizontal").pack(fill="x", pady=5)

    def show_add_device_dialog(self):
        """Show dialog to add a new device"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Device")
        dialog.geometry("400x500")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"400x500+{x}+{y}")

        # Main frame
        main_frame = ttk.Frame(dialog, style="Custom.TFrame", padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(main_frame, text="➕ Add New Device", 
                 style="Title.TLabel").pack(pady=(0, 20))

        # Device type selection
        ttk.Label(main_frame, text="Device Type:", style="Custom.TLabel").pack(pady=(0, 10))
        device_type = tk.StringVar(value="light")
        
        type_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        type_frame.pack(fill="x", pady=(0, 20))
        
        device_types = [
            ("💡 Light", "light"),
            ("🌡️ Thermostat", "thermostat"), 
            ("🔒 Smart Lock", "lock")
        ]
        
        for display_name, dtype in device_types:
            ttk.Radiobutton(type_frame, text=display_name, value=dtype,
                           variable=device_type, style="Mode.TRadiobutton").pack(anchor="w", pady=2)

        # Device details
        ttk.Label(main_frame, text="Device Name:", style="Custom.TLabel").pack(pady=(0, 5))
        name_entry = ttk.Entry(main_frame, width=40)
        name_entry.pack(pady=(0, 15))

        ttk.Label(main_frame, text="Location:", style="Custom.TLabel").pack(pady=(0, 5))
        location_entry = ttk.Entry(main_frame, width=40)
        location_entry.pack(pady=(0, 30))

        # Button frame
        btn_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        btn_frame.pack(fill="x")

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
                messagebox.showinfo("Success", f"{name} has been added successfully!")
            else:
                messagebox.showerror("Error", "Failed to add device")

        def cancel():
            dialog.destroy()

        ttk.Button(btn_frame, text="Add Device", command=add_device,
                  style="AddDevice.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(btn_frame, text="Cancel", command=cancel,
                  style="Logout.TButton").pack(side="left")

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