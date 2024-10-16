import tkinter as tk
from modules.ui import AuthScreen

if __name__ == "__main__":
    root = tk.Tk()
    auth = AuthScreen(root)
    root.mainloop()
