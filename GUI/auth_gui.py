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
from GUI.modern_home import ModernHomePage

class AuthGUI:
    def __init__(self):
        # Color scheme for consistency
        self.colors = {
            'primary': '#1976d2',
            'primary_hover': '#115293',
            'secondary': '#64748b',
            'success': '#059669',
            'danger': '#dc2626',
            'warning': '#d97706',
            'background': '#ffffff',
            'surface': '#f7f7f7',
            'text': '#222222',
            'text_secondary': '#888888',
            'border': '#e2e8f0'
        }
        
        self.root = tk.Tk()
        self.root.title("Smart Home Control System")
        self.root.geometry("500x600")
        self.root.configure(bg=self.colors['background'])
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"500x600+{x}+{y}")
        
        self.auth = UserAuth()
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure modern styles for widgets"""
        style = ttk.Style()
        
        # Frame styles
        style.configure("Custom.TFrame", background=self.colors['background'])
        style.configure("Card.TFrame", background=self.colors['surface'], relief="raised", borderwidth=1)
        
        # Label styles
        style.configure("Custom.TLabel", background=self.colors['background'], foreground=self.colors['text'], font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=self.colors['background'], foreground=self.colors['text'], font=("Segoe UI", 24, "bold"))
        style.configure("Subtitle.TLabel", background=self.colors['background'], foreground=self.colors['text_secondary'], font=("Segoe UI", 12))
        style.configure("Card.TLabel", background=self.colors['surface'], foreground=self.colors['text'], font=("Segoe UI", 10))
        style.configure("Link.TLabel", background=self.colors['surface'], foreground=self.colors['primary'], font=("Segoe UI", 10, "underline"))
        
        # Button styles
        style.configure("Primary.TButton", background=self.colors['primary'], foreground="white", font=("Segoe UI", 12, "bold"), borderwidth=0)
        style.map("Primary.TButton",
                  background=[('active', self.colors['primary_hover']), ('!active', self.colors['primary'])],
                  foreground=[('active', 'white'), ('!active', 'white')])
        style.configure("Secondary.TButton", background="#e0e0e0", foreground=self.colors['text'], font=("Segoe UI", 10))

    def create_widgets(self):
        """Create the main container and widgets"""
        self.main_frame = ttk.Frame(self.root, style="Custom.TFrame", padding="30")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title and subtitle
        title_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        title_frame.pack(pady=(0, 30))
        
        ttk.Label(title_frame, text="🏠 Smart Home", style="Title.TLabel").pack()
        ttk.Label(title_frame, text="Control System", style="Subtitle.TLabel").pack()

        # Login Card
        self.login_card = ttk.Frame(self.main_frame, style="Card.TFrame", padding="30")
        self.login_card.pack(fill="x", pady=(0, 20))

        # Login title
        ttk.Label(self.login_card, text="Welcome Back", style="Title.TLabel").pack(pady=(0, 20))

        # Username
        ttk.Label(self.login_card, text="Username:", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.username_entry = ttk.Entry(self.login_card, width=35, font=("Segoe UI", 11))
        self.username_entry.pack(fill="x", pady=(0, 15))

        # Password
        ttk.Label(self.login_card, text="Password:", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.password_entry = ttk.Entry(self.login_card, width=35, show="•", font=("Segoe UI", 11))
        self.password_entry.pack(fill="x", pady=(0, 25))

        # Login Button
        self.login_btn = ttk.Button(self.login_card, text="🔐 Login", command=self.login, style="Primary.TButton")
        self.login_btn.pack(fill="x", pady=(0, 20))
        self.login_btn.bind("<Enter>", self.on_login_hover)
        self.login_btn.bind("<Leave>", self.on_login_leave)

        # Signup Link
        signup_link = ttk.Label(self.login_card, text="Don't have an account? Sign up", 
                              style="Link.TLabel", cursor="hand2")
        signup_link.pack()
        signup_link.bind("<Button-1>", lambda e: self.show_signup())

        # Signup Card (initially hidden)
        self.signup_card = ttk.Frame(self.main_frame, style="Card.TFrame", padding="30")
        
        # Signup title
        ttk.Label(self.signup_card, text="Create Account", style="Title.TLabel").pack(pady=(0, 20))

        # Signup Username
        ttk.Label(self.signup_card, text="Choose Username:", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.signup_username_entry = ttk.Entry(self.signup_card, width=35, font=("Segoe UI", 11))
        self.signup_username_entry.pack(fill="x", pady=(0, 15))

        # Signup Password
        ttk.Label(self.signup_card, text="Choose Password:", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.signup_password_entry = ttk.Entry(self.signup_card, width=35, show="•", font=("Segoe UI", 11))
        self.signup_password_entry.pack(fill="x", pady=(0, 15))

        # Confirm Password
        ttk.Label(self.signup_card, text="Confirm Password:", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.confirm_password_entry = ttk.Entry(self.signup_card, width=35, show="•", font=("Segoe UI", 11))
        self.confirm_password_entry.pack(fill="x", pady=(0, 25))

        # Signup Button
        signup_btn = ttk.Button(self.signup_card, text="📝 Sign Up", command=self.signup, style="Primary.TButton")
        signup_btn.pack(fill="x", pady=(0, 20))

        # Login Link
        login_link = ttk.Label(self.signup_card, text="Already have an account? Login", 
                             style="Link.TLabel", cursor="hand2")
        login_link.pack()
        login_link.bind("<Button-1>", lambda e: self.show_login())

    def on_login_hover(self, event):
        self.login_btn.state(["active"])

    def on_login_leave(self, event):
        self.login_btn.state(["!active"])

    def show_signup(self):
        """Switch to signup view"""
        self.login_card.pack_forget()
        self.signup_card.pack(fill="x", pady=(0, 20))

    def show_login(self):
        """Switch to login view"""
        self.signup_card.pack_forget()
        self.login_card.pack(fill="x", pady=(0, 20))

    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        success, message = self.auth.login_user(username, password)
        if success:
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.root.withdraw()  # Hide the login window
            home_page = ModernHomePage(username, self.colors)
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
            # Clear the signup fields
            self.signup_username_entry.delete(0, tk.END)
            self.signup_password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", message)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AuthGUI()
    app.run() 