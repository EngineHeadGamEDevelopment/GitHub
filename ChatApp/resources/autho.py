import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
import asyncio
import threading
import json
import os
import bcrypt  # For password hashing

# Define paths for data sources
DATA_PATH = 'data'
USERS_FILE = 'users.json'

# Check and create necessary directories
os.makedirs(DATA_PATH, exist_ok=True)

class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Chat Interface")

        # Create a scrollable text area for displaying chat messages
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        # Create an entry field for user input
        self.input_field = tk.Entry(master, width=48)
        self.input_field.pack(padx=10, pady=5)

        # Create a button to send messages
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        # Create a label for the loading spinner
        self.spinner_label = tk.Label(master, text="", font=("Arial", 20), fg="blue")
        self.spinner_label.pack(pady=5)

        # Bind the return key to the send message function
        self.input_field.bind("<Return>", lambda event: self.send_message())

        # Flag to control the spinner state
        self.loading = False

    def send_message(self):
        """Send message from input field to chat area."""
        user_input = self.input_field.get()
        if user_input:
            self.chat_area.config(state='normal')  # Enable editing the chat area
            self.chat_area.insert(tk.END, f"You: {user_input}\n")  # Display user input
            self.chat_area.config(state='disabled')  # Disable editing
            self.chat_area.see(tk.END)  # Scroll to the end
            self.input_field.delete(0, tk.END)  # Clear input field
            
            # Start spinner animation on a separate thread
            threading.Thread(target=self.start_spinner).start()

            # Here you can call your asynchronous function for data fetching
            threading.Thread(target=self.process_command, args=(user_input,)).start()

    def process_command(self, command):
        """Process user command and fetch external data if needed."""
        self.start_spinner()  # Start spinner when fetching data
        time.sleep(3)  # Simulate a long-running task
        self.display_message(f"Processed command: {command}")
        self.stop_spinner()  # Stop spinner after task

    def display_message(self, message):
        """Display a message in the chat area."""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"AI: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def start_spinner(self):
        """Start the spinner animation."""
        self.loading = True
        spinner_sequence = ["|", "/", "-", "\\"]  # Customize spinner characters
        idx = 0

        while self.loading:
            self.spinner_label.config(text=spinner_sequence[idx % len(spinner_sequence)])
            idx += 1
            time.sleep(0.1)  # Adjust spinner speed
        self.spinner_label.config(text="")  # Clear spinner when done

    def stop_spinner(self):
        """Stop the spinner animation."""
        self.loading = False

class AuthScreen:
    """Authentication screen for login/signup."""

    def __init__(self, master):
        self.master = master
        self.master.title("User Authentication")

        # Create label and entry for username
        self.label_user = tk.Label(master, text="Username:")
        self.label_user.pack(pady=5)
        self.entry_user = tk.Entry(master)
        self.entry_user.pack(pady=5)

        # Create label and entry for password
        self.label_pass = tk.Label(master, text="Password:")
        self.label_pass.pack(pady=5)
        self.entry_pass = tk.Entry(master, show='*')
        self.entry_pass.pack(pady=5)

        # Create login and signup buttons
        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack(pady=5)
        self.signup_button = tk.Button(master, text="Signup", command=self.signup)
        self.signup_button.pack(pady=5)

    def login(self):
        """Handle user login."""
        username = self.entry_user.get()
        password = self.entry_pass.get()

        if username and password:
            if self.verify_credentials(username, password):
                messagebox.showinfo("Login Success", f"Welcome back, {username}!")
                self.master.destroy()  # Close auth screen and launch chat
                self.launch_chat_app()
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def signup(self):
        """Handle new user signup."""
        username = self.entry_user.get()
        password = self.entry_pass.get()

        if username and password:
            if self.user_exists(username):
                messagebox.showerror("Signup Failed", "Username already exists. Try another.")
            else:
                self.save_new_user(username, password)
                messagebox.showinfo("Signup Success", "Account created successfully!")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def user_exists(self, username):
        """Check if the user already exists."""
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                users = json.load(f)
            return username in users
        return False

    def verify_credentials(self, username, password):
        """Verify the user's credentials."""
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                users = json.load(f)

            if username in users:
                stored_hash = users[username]['password']
                return bcrypt.checkpw(password.encode(), stored_hash.encode())
        return False

    def save_new_user(self, username, password):
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

    def launch_chat_app(self):
        """Launch the chat application."""
        root = tk.Tk()
        chat_app = ChatApp(root)
        root.mainloop()

# Running the Auth Screen
if __name__ == "__main__":
    root = tk.Tk()
    auth_screen = AuthScreen(root)
    root.mainloop()
