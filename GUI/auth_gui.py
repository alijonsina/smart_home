import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from User.user_auth import UserAuth
from GUI.home_page import HomePage

class AuthGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Home Control System")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")
        
        self.auth = UserAuth()
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        style.configure("Custom.TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("Title.TLabel", background="#f0f0f0", font=("Helvetica", 16, "bold"))
        style.configure("Custom.TButton", font=("Helvetica", 10))
        style.configure("Link.TLabel", background="#f0f0f0", font=("Helvetica", 9, "underline"), foreground="blue")

    def create_widgets(self):
        """Create the main container and widgets"""
        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame", padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(self.main_frame, text="Smart Home Control", style="Title.TLabel")
        title_label.pack(pady=20)

        # Login Frame
        self.login_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Username
        ttk.Label(self.login_frame, text="Username:", style="Custom.TLabel").pack(pady=(0, 5))
        self.username_entry = ttk.Entry(self.login_frame, width=30)
        self.username_entry.pack(pady=(0, 10))

        # Password
        ttk.Label(self.login_frame, text="Password:", style="Custom.TLabel").pack(pady=(0, 5))
        self.password_entry = ttk.Entry(self.login_frame, width=30, show="•")
        self.password_entry.pack(pady=(0, 20))

        # Login Button
        login_btn = ttk.Button(self.login_frame, text="Login", command=self.login, style="Custom.TButton")
        login_btn.pack(pady=(0, 10))

        # Signup Link
        signup_link = ttk.Label(self.login_frame, text="Don't have an account? Sign up", 
                              style="Link.TLabel", cursor="hand2")
        signup_link.pack(pady=(10, 0))
        signup_link.bind("<Button-1>", lambda e: self.show_signup())

        # Signup Frame (initially hidden)
        self.signup_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        
        # Signup Username
        ttk.Label(self.signup_frame, text="Choose Username:", style="Custom.TLabel").pack(pady=(0, 5))
        self.signup_username_entry = ttk.Entry(self.signup_frame, width=30)
        self.signup_username_entry.pack(pady=(0, 10))

        # Signup Password
        ttk.Label(self.signup_frame, text="Choose Password:", style="Custom.TLabel").pack(pady=(0, 5))
        self.signup_password_entry = ttk.Entry(self.signup_frame, width=30, show="•")
        self.signup_password_entry.pack(pady=(0, 10))

        # Confirm Password
        ttk.Label(self.signup_frame, text="Confirm Password:", style="Custom.TLabel").pack(pady=(0, 5))
        self.confirm_password_entry = ttk.Entry(self.signup_frame, width=30, show="•")
        self.confirm_password_entry.pack(pady=(0, 20))

        # Signup Button
        signup_btn = ttk.Button(self.signup_frame, text="Sign Up", command=self.signup, style="Custom.TButton")
        signup_btn.pack(pady=(0, 10))

        # Login Link
        login_link = ttk.Label(self.signup_frame, text="Already have an account? Login", 
                             style="Link.TLabel", cursor="hand2")
        login_link.pack(pady=(10, 0))
        login_link.bind("<Button-1>", lambda e: self.show_login())

    def show_signup(self):
        """Switch to signup view"""
        self.login_frame.pack_forget()
        self.signup_frame.pack(fill=tk.BOTH, expand=True)

    def show_login(self):
        """Switch to login view"""
        self.signup_frame.pack_forget()
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        success, message = self.auth.login_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.root.withdraw()  # Hide the login window
            home_page = HomePage(username)
            home_page.run()
            self.root.destroy()  # Destroy the login window after home page is closed
        else:
            messagebox.showerror("Error", message)

    def signup(self):
        """Handle signup attempt"""
        username = self.signup_username_entry.get().strip()
        password = self.signup_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        success, message = self.auth.register_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.show_login()
        else:
            messagebox.showerror("Error", message)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AuthGUI()
    app.run() 