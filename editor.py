from tkinter import ttk
import tkinter as tk  # Import the tkinter module
import os  # Import the os module
import ttkbootstrap as ttkb  # Import the ttkbootstrap module
from tkinter import filedialog  # Import the filedialog module
import re  # Import the re module
import threading
import toml
import subprocess

filecontents = ""  # Create a variable to store the file contents

# Determine the directory where the script is located to locate files in its own directory (It won't load the icon/theme unless I do this)
script_dir = os.path.dirname(__file__)  # Get the directory where the script is located

def debounce(wait):
    """ Decorator that will postpone a function's
        execution until after `wait` seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            if hasattr(debounced, '_timer'):
                debounced._timer.cancel()
            debounced._timer = threading.Timer(wait, call_it)
            debounced._timer.start()
        return debounced
    return decorator

def readfile():
    if filecontentstext.cget('state') == 'disabled':  # If the text widget is disabled
        filecontentstext.config(state='normal', fg='white')
    global filecontents  # Declare filecontents as global
    file_path = filedialog.askopenfilename()  # Get the path to the file
    with open(file_path, 'r') as file:  # Open the file
        filecontents = file.read()  # Read the file
    filecontentstext.insert(tk.END, filecontents)  # Insert the file contents into the text widget
    filecontentstext.config(state='disabled', fg='gray')  # Disable the text widget and set the text color to gray
    textboxlist()
        
def textboxlist():
    global filecontents  # Declare filecontents as global
    matches = re.findall(r'\"(.*?)\":(.*?),', filecontents)  # Find all occurrences of text between a ":" and a ","
    textbox_frame = ttk.Frame(master=window)  # Create a new frame for the textboxes
    
    # Create a search bar
    search_var = tk.StringVar()
    ttk.Label(master=textbox_frame, text="Search:").pack(pady=10)
    search_entry = ttk.Entry(master=textbox_frame, textvariable=search_var)
    search_entry.pack()
    search_var.trace("w", lambda *args: filter_labels(search_var.get(), labels))
    
    # Create a scrollable canvas
    canvas = tk.Canvas(textbox_frame, width=600)
    scrollbar = ttk.Scrollbar(textbox_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    textbox_frame.pack()  # Add the frame to the window
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    labels = []
    row = 0
    for label_text, match in matches:
        text_var = tk.StringVar()
        text_var.set(match)
        label = ttk.Label(master=scrollable_frame, text=label_text)
        label.grid(row=row, column=0, pady=5)  # Add the label to the grid with vertical spacing of 5
        # Create a dropdown selector for boolean values
        if match.lower() in ['true', 'false']:
            bool_var = tk.BooleanVar()
            bool_var.set(match.lower() == 'true')
            bool_selector = ttk.Checkbutton(master=scrollable_frame, variable=bool_var)
            bool_selector.grid(row=row, column=1, pady=5)  # Add the bool selector to the grid with vertical spacing of 5
            bool_var.trace("w", lambda *args, label_text=label_text, bool_var=bool_var: update_filecontents_bool(label_text, bool_var))
            labels.append((label, bool_selector))
        else:
            textbox = ttk.Entry(master=scrollable_frame, textvariable=text_var, width=10)
            textbox.label_text = label_text
            textbox.grid(row=row, column=1, pady=5)
            save_button = ttk.Button(master=scrollable_frame, text="Save", command=lambda label_text=label_text, text_var=text_var: update_filecontents_text(label_text, text_var))
            save_button.grid(row=row, column=2, pady=5)
            labels.append((label, textbox, save_button))
        row += 1
    
    # Bind the scroll wheel to the canvas
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

def update_filecontents_text(label_text, text_var):
    global filecontents  # Declare filecontents as global
    new_text = str(text_var.get())
    temp = re.sub(rf'"{label_text}":.*?,', f'"{label_text}":{new_text.strip()},', filecontents)
    filecontents = temp
    filecontentstext.config(state='normal')  # Enable the text widget
    filecontentstext.delete(1.0, tk.END)
    filecontentstext.insert(tk.END, filecontents)
    filecontentstext.config(state='disabled')  # Disable the text widget

def update_filecontents_bool(label_text, bool_var):
    global filecontents  # Declare filecontents as global
    new_text = str(bool_var.get()).lower()
    filecontents = re.sub(rf'"{label_text}":(.*?),', f'"{label_text}":{new_text},', filecontents)
    filecontentstext.config(state='normal')  # Enable the text widget
    filecontentstext.delete(1.0, tk.END)
    filecontentstext.insert(tk.END, filecontents)
    filecontentstext.config(state='disabled')  # Disable the text widget
    
@debounce(0.3)
def filter_labels(search_text, labels):
    for label_tuple in labels:
        save_button = None  # Initialize save_button to None
        if len(label_tuple) == 2:
            label, textbox = label_tuple
        elif len(label_tuple) == 3:
            label, textbox, save_button = label_tuple
        if search_text.lower() in label.cget("text").lower():
            label.grid()
            textbox.grid()
            if save_button:
                save_button.grid()
        else:
            label.grid_remove()
            textbox.grid_remove()
            if save_button:
                save_button.grid_remove()

def savefile():
    global filecontents  # Declare filecontents as global
    file_path = filedialog.asksaveasfilename(defaultextension=".json")  # Get the path to save the file
    with open(file_path, 'w') as file:  # Open the file in write mode
        file.write(filecontentstext.get("1.0", tk.END))  # Write the contents of the text widget to the file
        tk.messagebox.showinfo("Success", "File saved successfully")  # Show a message box with the success message
        subprocess.Popen(["python", os.path.join(script_dir, 'Main-RUNTHIS.py')], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        exit()  # Exit the program

# Load and read the settings.toml file
settings_file = os.path.join(script_dir, "settings.toml")
with open(settings_file, "r") as f:
    settings = toml.load(f)

# Get the theme setting from the settings file
theme = settings.get("theme", "default")

# Create the main window with the specified theme
window = ttkb.Window(themename=theme)
window.title("SCSettings Editor")  # Set the window title
window.geometry('1000x800')  # Set the initial window size

# Set the window icon
icon_path = os.path.join(script_dir, "stolenlogo.ico")  # Get the path to the icon
window.iconbitmap(icon_path)  # Set the window icon using the iconbitmap method because things break If I don't

# Create the title label
title_label = ttk.Label(master=window, text="Editor", font='Calibri 24 bold')  # Create a label with the title
title_label.pack()  # Add the label to the window

# File contents displayed as text
filecontentsframe = ttk.Frame(master=window)
filecontentstext = tk.Text(master=filecontentsframe, width=150, height=20, undo=True)
filecontentstext.pack()
filecontentsframe.pack(pady=20)

# Create the menu buttons
buttons_frame = ttk.Frame(master=window)  # Create a frame for the buttons
openfilebutton = ttk.Button(master=buttons_frame, text='Open File', command=readfile)  # Create a settings button
savefilebutton = ttk.Button(master=buttons_frame, text='Save File', command=savefile)  # Create a save file button
openfilebutton.pack(side="left", padx=5)  # Add the settings button to the frame
savefilebutton.pack(side="left")  # Add the save file button to the frame
buttons_frame.pack(pady=20)  # Add the frame to the window

# Start the application
window.mainloop()  # Start the tkinter event loop
