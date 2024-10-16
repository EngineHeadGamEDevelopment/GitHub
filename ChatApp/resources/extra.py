import tkinter as tk
from tkinter import messagebox
import asyncio
import threading
import time

class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Chat Interface")

        # Create a scrollable text area for displaying chat messages
        self.chat_area = tk.Text(master, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        # Create an entry field for user input
        self.input_field = tk.Entry(master, width=48)
        self.input_field.pack(padx=10, pady=5)

        # Create a button to send messages
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        # Create a label to show the loading spinner
        self.loading_label = tk.Label(master, text="")
        self.loading_label.pack(pady=5)

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
        self.start_loading_spinner()  # Start spinner when fetching data
        time.sleep(2)  # Simulate a time-consuming process
        self.stop_loading_spinner()  # Stop spinner after the process
        self.display_message(f"Processed: {command}")

    def display_message(self, message):
        """Display a message in the chat area."""
