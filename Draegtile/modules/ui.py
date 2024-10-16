from datetime import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import asyncio
from modules.api import fetch_weather
from modules.auth import verify_credentials, save_new_user, user_exists

class DraegtileApp:
    def __init__(self, master):
        self.master = master
        master.title("Draegtile Chat Interface")

        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        self.input_field = tk.Entry(master, width=48)
        self.input_field.pack(padx=10, pady=5)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.spinner_label = tk.Label(master, text="", font=("Arial", 20), fg="blue")
        self.spinner_label.pack(pady=5)

        self.input_field.bind("<Return>", lambda event: self.send_message())
        self.loading = False

    def send_message(self):
        """Send message and process input."""
        user_input = self.input_field.get()
        if user_input:
            self.add_to_chat(f"You: {user_input}")
            self.input_field.delete(0, tk.END)

            # Process the command and fetch data (e.g., weather)
            if user_input.startswith("weather"):
                city = user_input.split(" ")[1]
                threading.Thread(target=self.process_weather, args=(city,)).start()

    def add_to_chat(self, message):
        """Add messages to the chat area."""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def process_weather(self, city):
        """Fetch weather data asynchronously."""
        asyncio.run(self.fetch_and_display_weather(city))

    async def fetch_and_display_weather(self, city):
        self.start_spinner()
        data = await fetch_weather(city)
        if data:
            weather_info = f"Weather in {city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
            self.add_to_chat(f"AI: {weather_info}")
        else:
            self.add_to_chat("AI: Failed to retrieve weather data.")
        self.stop_spinner()

    def start_spinner(self):
        """Display a spinner animation."""
        self.loading = True
        spinner_sequence = ["|", "/", "-", "\\"]
        idx = 0
        while self.loading:
            self.spinner_label.config(text=spinner_sequence[idx % len(spinner_sequence)])
            idx += 1
            time.sleep(0.1)

    def stop_spinner(self):
        """Stop the spinner."""
        self.loading = False
        self.spinner_label.config(text="")

class AuthScreen:
    def __init__(self, master):
        self.master = master
        master.title("Draegtile Authentication")

        tk.Label(master, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)

        tk.Label(master, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(master, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(master, text="Login", command=self.login).pack(pady=5)
        tk.Button(master, text="Signup", command=self.signup).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if verify_credentials(username, password):
            messagebox.showinfo("Login Success", f"Welcome {username}")
            self.master.destroy()
            self.launch_chat()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if user_exists(username):
            messagebox.showerror("Error", "User already exists")
        else:
            save_new_user(username, password)
            messagebox.showinfo("Signup Success", "User registered successfully")

    def launch_chat(self):
        root = tk.Tk()
        app = DraegtileApp(root)
        root.mainloop()
