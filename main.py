# main.py
import tkinter as tk
from src.app import WasteManagementApp

if __name__ == "__main__":
    root = tk.Tk()
    app = WasteManagementApp(root)
    root.mainloop()
