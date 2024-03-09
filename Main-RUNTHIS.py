import importlib
import subprocess
import sys

REQUIRED_PACKAGES = ['toml', 'ttkbootstrap']

for package in REQUIRED_PACKAGES:
    try:
        importlib.import_module(package)
        print(f'{package} is installed')
    except ImportError:
        print(f'{package} is NOT installed')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

from tkinter import ttk
import toml
import os  # Import the os module
import subprocess  # Import the subprocess module
import ttkbootstrap as ttkb  # Import the ttkbootstrap module

# Determine the directory where the script is located to locate files in its own directory (It won't load the icon/theme unless I do this)
script_dir = os.path.dirname(__file__)  # Get the directory where the script is located

# Rest of the code...

# Determine the directory where the script is located to locate files in its own directory (It won't load the icon/theme unless I do this)
script_dir = os.path.dirname(__file__)  # Get the directory where the script is located

# Run settings.py
def exec_settings():
    subprocess.Popen(["python", os.path.join(script_dir, 'settings.py')], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    exit()

def exec_editor():
    subprocess.Popen(["python", os.path.join(script_dir, 'editor.py')], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    exit()

# Load and read the settings.toml file
settings_file = os.path.join(script_dir, "settings.toml")
with open(settings_file, "r") as f:
    settings = toml.load(f)

# Get the theme setting from the settings file
theme = settings.get("theme", "default")

# Create the main window with the specified theme
window = ttkb.Window(themename=theme)
window.title("SCSettings")  # Set the window title
window.geometry('250x400')  # Set the initial window size

# Set the window icon
icon_path = os.path.join(script_dir, "stolenlogo.ico")  # Get the path to the icon
window.iconbitmap(icon_path)  # Set the window icon using the iconbitmap method because ttkthemes doesn't like the regular one

# Create the title label
title_label = ttk.Label(master=window, text='Main Menu', font='Calibri 24 bold')  # Create a label with the title
title_label.pack()  # Add the label to the window

# Create the menu buttons
buttons_frame = ttk.Frame(master=window)  # Create a frame for the buttons
editorbutton = ttk.Button(master=buttons_frame, text='JSON Editor', command=exec_editor)  # Create a settings button
settingsbutton = ttk.Button(master=buttons_frame, text='Settings', command=exec_settings)  # Create a settings button
editorbutton.pack(pady=5)  # Add the editor button to the frame
settingsbutton.pack(pady=5)  # Add the settings button to the frame
buttons_frame.pack(pady=20)  # Add the frame to the window

# Start the application
window.mainloop()  # Start the tkinter event loop
