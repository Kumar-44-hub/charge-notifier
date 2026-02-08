import tkinter as tk
from tkinter import messagebox

def show_full_charge_popup():
    root = tk.Tk()
    root.title("Charge Notifier")

    # Keep window on top
    root.attributes("-topmost", True)

    # Hide main Tk window
    root.withdraw()

    # This BLOCKS until user clicks OK
    messagebox.showinfo(
        "Charge Notifier",
        "Battery fully charged (100%).\nPlease unplug the charger."
    )

    root.destroy()
