
import tkinter as tk
from tkinter import ttk, filedialog
import threading

def load_json(filename):
    data = {}
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            entries = [entry.strip() for entry in line.split(',') if ':' in entry]
            for entry in entries:
                key, value = entry.split(':', 1)
                data[key.strip().strip('"')] = value.strip(), line_number
    return data

def create_index(data):
    index = {}
    for key, (value, line_number) in data.items():
        identifier = f"{key}:{value}"
        if identifier in index:
            index[identifier].append(line_number)
        else:
            index[identifier] = [line_number]
    return index

def open_file(scrollable_frame, entries, root):
    global filename
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if filename:
        root.title("JSON Data Editor - Loading...")
        for entry in entries.values():
            entry.destroy()
        threading.Thread(target=read_and_display_chunks, args=(filename, scrollable_frame, entries, root)).start()

def read_and_display_chunks(filename, scrollable_frame, entries, root):
    chunk_size = 1000
    chunks = []
    total_lines = sum(1 for line in open(filename))
    lines_processed = 0

    with open(filename, 'r') as file:
        chunk = []
        for line in file:
            lines_processed += 1
            chunk.append(line)
            if len(chunk) >= chunk_size:
                chunks.append(chunk)
                chunk = []
                scrollable_frame.update_idletasks()
        if chunk:
            chunks.append(chunk)

    data = {}
    for chunk in chunks:
        data.update(load_json_from_chunk(chunk))

    index = create_index(data)
    update_editor(data, index, scrollable_frame, entries, root)

def load_json_from_chunk(chunk):
    data = {}
    for line_number, line in enumerate(chunk, start=1):
        line = line.split('#', 1)[0].strip()
        if line:
            entries = [entry.strip() for entry in line.split(',') if ':' in entry]
            for entry in entries:
                key, value = entry.split(':', 1)
                data[key.strip().strip('"')] = value.strip(), line_number
    return data

def update_editor(data, index, scrollable_frame, entries, root):
    false_width = len("false") * 2

    row_number = 0

    for key, (value, line_number) in data.items():
        label = ttk.Label(scrollable_frame, text=f"{key}:")
        label.grid(row=row_number, column=0, sticky="w")

        entry = ttk.Combobox(scrollable_frame, values=["true", "false"], width=false_width) if value.lower() in ["true", "false"] else ttk.Entry(scrollable_frame, width=false_width * 2)
        entry.grid(row=row_number, column=1, padx=5, pady=5)
        entry.insert(tk.END, value)
        entries[key] = entry

        row_number += 1

    root.title("JSON Data Editor")

def clear_entries(entries):
    for entry in entries.values():
        entry.destroy()
    entries.clear()
    for widget in scrollable_frame.winfo_children():
        if isinstance(widget, ttk.Label):
            widget.destroy()

def save_changes(entries):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for key, entry in entries.items():
        for i, line in enumerate(lines):
            if f'"{key}"' in line:
                value_start = line.find(':', line.find(f'"{key}"')) + 1
                value_end = line.find(',', value_start)
                if value_end == -1:
                    value_end = len(line)
                lines[i] = line[:value_start] + entry.get() + line[value_end:]
                break

    with open(filename, 'w') as file:
        file.writelines(lines)

def search_entries(entries, search_text, index):
    search_text = search_text.lower()
    for identifier, line_numbers in index.items():
        if search_text in identifier.lower():
            for line_number in line_numbers:
                entry = entries.get(line_number)
                if entry:
                    entry.config(state=tk.NORMAL)
        else:
            for line_number in line_numbers:
                entry = entries.get(line_number)
                if entry:
                    entry.config(state=tk.DISABLED)

def toggle_entry_state(entry):
    entry.config(state=tk.NORMAL) if entry["state"] == tk.DISABLED else None

def clear_search_and_search_entries(event, entry, entries, search_var):
    for entry in entries.values():
        entry.config(state=tk.NORMAL)
    search_var.set("")

def create_editor():
    root = tk.Tk()
    root.title("JSON Data Editor")
    root.geometry("840x560")

    global canvas
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    global scrollable_frame
    scrollable_frame = ttk.Frame(canvas)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame.grid_rowconfigure(scrollable_frame.grid_size()[1], weight=1)

    entries = {}

    search_var = tk.StringVar()
    search_entry = ttk.Entry(root, textvariable=search_var, width=30)
    search_entry.pack(pady=5)
    search_button = ttk.Button(root, text="Search", command=lambda: search_entries(entries, search_var.get(), index))
    search_button.pack(pady=5)

    ttk.Button(root, text="Open File", command=lambda: open_file(scrollable_frame, entries, root)).pack(pady=5)
    ttk.Button(root, text="Clear Entries", command=lambda: clear_entries(entries)).pack(pady=5)
    ttk.Button(root, text="Save Changes", command=lambda: save_changes(entries)).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    create_editor()
