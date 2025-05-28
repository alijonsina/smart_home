import json
import os
import hashlib
from typing import Tuple, Optional

class UserAuth:
    def __init__(self):
        self.users_file = os.path.join(os.path.dirname(__file__), 'users.json')
        self._ensure_users_file()

    def _ensure_users_file(self):
        """Create users.json file if it doesn't exist"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user
        Returns: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password cannot be empty"

        if len(password) < 6:
            return False, "Password must be at least 6 characters long"

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        if username in users:
            return False, "Username already exists"

        hashed_password = self._hash_password(password)
        users[username] = hashed_password

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        return True, "Registration successful"

    def login_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate a user
        Returns: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password cannot be empty"

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        if username not in users:
            return False, "User not found"

        hashed_password = self._hash_password(password)
        if users[username] != hashed_password:
            return False, "Invalid password"

        return True, "Login successful" 