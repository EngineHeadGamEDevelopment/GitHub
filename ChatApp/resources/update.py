import json
import os
import requests
import asyncio
import bcrypt  # For password hashing
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time  # Importing time module

# Define paths for data sources
DATA_PATH = 'data'
USERS_FILE = 'users.json'

# Check and create necessary directories
os.makedirs(DATA_PATH, exist_ok=True)

# Sample API Keys
API_KEYS = {
    'weather': "8db9fee751e3fa5a3596c9cc96486f91",
    'news': "e18eb01c2b3d45908104628792035eeb",
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

        # Create a frame for buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        # Create buttons for different data options
        self.create_option_button("Weather", self.fetch_weather)
        self.create_option_button("News", self.fetch_news)
        self.create_option_button("Currency", self.fetch_currency)
        self.create_option_button("Stock", self.fetch_stock)
        self.create_option_button("Timezone", self.fetch_timezone)

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

    def create_option_button(self, label, command):
        """Create a button with a chat bubble style."""
        button = tk.Button(self.button_frame, text=label, command=command, width=12, bg="#4CAF50", fg="white")
        button.pack(side=tk.LEFT, padx=5, pady=5)

    def send_message(self):
        """Send message from input field to chat area."""
        user_input = self.input_field.get()
        if user_input:
            self.chat_area.config(state='normal')  # Enable editing the chat area
            self.chat_area.insert(tk.END, f"You: {user_input}\n")  # Display user input
            self.chat_area.config(state='disabled')  # Disable editing
            self.chat_area.see(tk.END)  # Scroll to the end
            self.input_field.delete(0, tk.END)  # Clear input field
            
            # Start spinner animation
            self.loading = True
            self.spinner_thread = threading.Thread(target=self.start_spinner)
            self.spinner_thread.start()

            # Here you can call your asynchronous function for data fetching
            threading.Thread(target=self.process_command, args=(user_input,)).start()

    def process_command(self, command):
        """Process user command and fetch external data if needed."""
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
        spinner_sequence = ["|", "/", "-", "\\"]  # Customize spinner characters
        idx = 0

        while self.loading:
            self.master.after(0, self.spinner_label.config, {'text': spinner_sequence[idx % len(spinner_sequence)]})
            idx += 1
            time.sleep(0.1)  # Adjust spinner speed
        self.master.after(0, self.spinner_label.config, {'text': ""})  # Clear spinner when done

    def stop_spinner(self):
        """Stop the spinner animation."""
        self.loading = False

    def fetch_weather(self):
        """Fetch weather data based on user input."""
        city = self.input_field.get()
        if city:
            threading.Thread(target=self.fetch_weather_data, args=(city,)).start()
        else:
            messagebox.showwarning("Input Error", "Please enter a city name.")

    def fetch_news(self):
        """Fetch news data."""
        threading.Thread(target=self.fetch_news_data).start()

    def fetch_currency(self):
        """Fetch currency exchange data."""
        base_currency = self.input_field.get() if self.input_field.get() else "USD"
        threading.Thread(target=self.fetch_currency_data, args=(base_currency,)).start()

    def fetch_stock(self):
        """Fetch stock data."""
        symbol = self.input_field.get()
        if symbol:
            threading.Thread(target=self.fetch_stock_data, args=(symbol,)).start()
        else:
            messagebox.showwarning("Input Error", "Please enter a stock symbol.")

    def fetch_timezone(self):
        """Fetch timezone data."""
        threading.Thread(target=self.fetch_timezone_data).start()

    # Fetch functions (assuming the APIs are set correctly)
    def fetch_weather_data(self, city):
        """Fetch weather data for the specified city."""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEYS['weather']}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_info = f"Weather in {data['name']}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
                self.display_message(weather_info)
            else:
                self.display_message(f"Failed to fetch weather data. Status Code: {response.status_code}")
        except Exception as e:
            self.display_message(f"Error fetching weather data: {e}")

    def fetch_news_data(self):
        """Fetch the latest news data."""
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEYS['news']}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data['articles'][:5]  # Top 5 articles
                articles_list = '\n'.join([f"- {article['title']}" for article in articles])
                self.display_message(f"Latest news:\n{articles_list}")
            else:
                self.display_message(f"Failed to fetch news data. Status Code: {response.status_code}")
        except Exception as e:
            self.display_message(f"Error fetching news data: {e}")

    def fetch_currency_data(self, base_currency):
        """Fetch currency exchange rates."""
        try:
            url = f"https://v6.exchangerate-api.com/v6/{API_KEYS['currency']}/latest/{base_currency}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                rates_list = '\n'.join([f"{currency}: {rate}" for currency, rate in data['conversion_rates'].items()])
                self.display_message(f"Currency exchange rates:\n{rates_list}")
            else:
                self.display_message(f"Failed to fetch currency exchange data. Status Code: {response.status_code}")
        except Exception as e:
            self.display_message(f"Error fetching currency exchange data: {e}")

    def fetch_stock_data(self, symbol):
        """Fetch stock data from Alpha Vantage."""
        try:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEYS['stock']}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                stock_info = "\n".join(
                    [f"{time}: Open: {info['1. open']}, High: {info['2. high']}, Low: {info['3. low']}, Close: {info['4. close']}" 
                     for time, info in data['Time Series (5min)'].items()][:5]
                )
                self.display_message(f"Stock data for {symbol}:\n{stock_info}")
            else:
                self.display_message(f"Failed to fetch stock data. Status Code: {response.status_code}")
        except Exception as e:
            self.display_message(f"Error fetching stock data: {e}")

    def fetch_timezone_data(self):
        """Fetch timezone data for the user's location."""
        try:
            url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEYS['timezone']}&format=json&by=position&lat=40.730610&lng=-73.935242"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                timezone_info = f"Timezone data: {json.dumps(data, indent=4)}"
                self.display_message(timezone_info)
            else:
                self.display_message(f"Failed to fetch timezone data. Status Code: {response.status_code}")
        except Exception as e:
            self.display_message(f"Error fetching timezone data: {e}")

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
