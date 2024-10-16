import tkinter as tk
from tkinter import scrolledtext
import threading
import time

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
        """Process user command (simulate a long task)."""
        time.sleep(3)  # Simulate long-running task
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

# Running the Chat App
if __name__ == "__main__":
    root = tk.Tk()
    chat_app = ChatApp(root)
    root.mainloop()
