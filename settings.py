import os
import toml
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb  # Import the ttkbootstrap module
import subprocess
import webbrowser

lightthemes = "https://ttkbootstrap.readthedocs.io/en/latest/themes/light/"
darkthemes = "https://ttkbootstrap.readthedocs.io/en/latest/themes/dark/"


# Determine the directory where the script is located
script_dir = os.path.dirname(__file__)
settings_file = os.path.join(script_dir, "settings.toml")

def exec_main():
    subprocess.Popen(["python", os.path.join(script_dir, 'Main-RUNTHIS.py')], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    exit()
    
# Load settings from the TOML file
def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            return toml.load(f)
    else:
        return {}
    
def open_urls():
    webbrowser.open(lightthemes)
    webbrowser.open(darkthemes)

# Save settings to the TOML file
def save_settings(settings):
    with open(settings_file, 'w') as f:
        toml.dump(settings, f)

# Load and read the settings.toml file
settings_file = os.path.join(script_dir, "settings.toml")
with open(settings_file, "r") as f:
    settings = toml.load(f)

# Get the theme setting from the settings file
theme = settings.get("theme", "default")

# Create the main window with the specified theme
window = ttkb.Window(themename=theme)
window.title("Settings")

# Set the window icon
icon_path = os.path.join(script_dir, "stolenlogo.ico")  # Get the path to the icon
window.iconbitmap(icon_path)  # Set the window icon using the iconbitmap method because ttkthemes doesn't like the regular one

# Load the settings
settings = load_settings()

# Create a dropdown menu for the theme setting
theme_setting = tk.StringVar()
theme_setting.set(theme)
theme_label = ttk.Label(window, text='Theme Setting (Requires restart)')
theme_default = ttk.Label(window, text='Default: Solar', font=("Calibri", 10, "italic"))
theme_label.pack()
theme_default.pack()
theme_dropdown = ttk.Combobox(window, textvariable=theme_setting, values=["solar", "superhero"])
theme_dropdown.pack()

# Create a save button
def save():
    settings['theme'] = theme_setting.get()
    save_settings(settings)
    exec_main()
    
    

more_settings_label = ttk.Label(window, text="More settings probably coming at some point.\n \n Badger me for them on the forums or my github.", font=("Calibri", 10, "italic"))
more_settings_label.pack(pady=10)
save_button = ttk.Button(window, text='Save Settings', command=save)
save_button.pack(pady=10)
ttk.Button(window, text="You can type your own themes into the theme selector!\n Click this to open the theme lists", command=open_urls).pack(pady=10)



window.mainloop()