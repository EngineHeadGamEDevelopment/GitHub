import json
import os
import bcrypt
from tkinter import messagebox

USERS_FILE = 'data/users.json'

def user_exists(username):
    """Check if the user already exists."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        return username in users
    return False

def verify_credentials(username, password):
    """Verify the user's credentials."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)

        if username in users:
            stored_hash = users[username]['password']
            return bcrypt.checkpw(password.encode(), stored_hash.encode())
    return False

def save_new_user(username, password):
    """Save a new user's credentials."""
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = {username: {'password': hashed_password}}

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = {}

    users.update(new_user)

    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
