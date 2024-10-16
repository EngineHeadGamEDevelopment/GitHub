import tkinter as tk
from tkinter import scrolledtext, messagebox
import asyncio
import threading
import json
import os
import bcrypt  # For password hashing
import requests
from datetime import datetime

# Define paths for data sources
DATA_PATH = 'data'
USERS_FILE = 'users.json'
ASSETS_PATH = 'assets'

# Check and create necessary directories
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(ASSETS_PATH, exist_ok=True)

# Sample data structures
external_api_data = {
    'weather': {},
    'news': {},
    'geological': {},
    'currency': {},
    'stock': {},
    'timezone': {}
}

# API keys (replace with your actual keys)
API_KEYS = {
    'weather': "8db9fee751e3fa5a3596c9cc96486f91",
    'news': "e18eb01c2b3d45908104628792035eeb",
    'geological': "ee8f7ba8bbfed94c77099072bd5be2d9",
    'currency': "2b908120946bfb453a18339c",
    'stock': "D8WS72X9TI9FZMH7",
    'timezone': "5KJZ0PM66RNQ"
}

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

        # Bind the return key to the send message function
        self.input_field.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        """Send message from input field to chat area."""
        user_input = self.input_field.get()
        if user_input:
            self.chat_area.config(state='normal')  # Enable editing the chat area
            self.chat_area.insert(tk.END, f"You: {user_input}\n")  # Display user input
            self.chat_area.config(state='disabled')  # Disable editing
            self.chat_area.see(tk.END)  # Scroll to the end
            self.input_field.delete(0, tk.END)  # Clear input field
            
            # Here you can call your asynchronous function
            threading.Thread(target=self.process_command, args=(user_input,)).start()

    def process_command(self, command):
        """Process user command and fetch external data if needed."""
        asyncio.run(self.fetch_external_data(command))

    async def fetch_external_data(self, command):
        """Asynchronously fetch external data from APIs and display results."""
        if command.startswith("weather"):
            city = command.split(" ")[1] if len(command.split(" ")) > 1 else None
            if city:
                await self.fetch_weather_data(city)
            else:
                self.display_message("Please provide a city name for weather data.")
        elif command == "news":
            await self.fetch_news_data()
        elif command == "geological":
            await self.fetch_geological_data()
        elif command.startswith("currency"):
            base_currency = command.split(" ")[1] if len(command.split(" ")) > 1 else "USD"
            await self.fetch_currency_exchange_data(base_currency)
        elif command.startswith("stock"):
            symbol = command.split(" ")[1] if len(command.split(" ")) > 1 else None
            if symbol:
                await self.fetch_stock_data(symbol)
            else:
                self.display_message("Please provide a stock symbol.")
        elif command == "timezone":
            await self.fetch_timezone_data()
        else:
            self.display_message("Unknown command. Please try again.")

    def display_message(self, message):
        """Display a message in the chat area."""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"AI: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    async def fetch_weather_data(self, city):
        """Fetch weather data for a specified city."""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEYS['weather']}&units=metric"
            response = await asyncio.to_thread(requests.get, url)
            if response.status_code == 200:
                data = response.json()
                external_api_data['weather'] = data
                self.save_data(external_api_data, 'external_api_data.json')
                self.display_message(f"Weather in {data['name']}: {data['main']['temp']}°C, {data['weather'][0]['description']}")
            else:
                self.display_message(f"Failed to fetch weather data. Status Code: {response.status_code}")

        except Exception as e:
            self.display_message(f"Error fetching weather data: {e}")

    def save_data(self, data, filename):
        """Save external API data to a JSON file."""
        with open(os.path.join(DATA_PATH, filename), 'w') as f:
            json.dump(data, f, indent=4)


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

        users
