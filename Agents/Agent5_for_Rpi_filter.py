import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3
import pyperclip

# Connect to SQLite database
DB_PATH = r'C:\Users\BRU09\Downloads\CRE-CRE_devices_Tracker_db_attempt1.db'

def connect_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to connect: {e}")
        return None

def filter_data():
    device_string = entry.get()
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()
    query = 'SELECT * FROM CRE_CRE_devices_Tracker_CSV WHERE "Devices Present" LIKE ?'
    cursor.execute(query, ('%' + device_string + '%',))
    results = cursor.fetchall()
    
    output_box.delete('1.0', tk.END)  # Clear previous results
    
    if results:
        column_names = [desc[0] for desc in cursor.description]  # Get column headers

        for result in results:
            rpi_label, devices_present, remarks, in_use_by = result[2], result[3], result[11], result[12]
            output_box.insert(tk.END, f"Rpi Label: {rpi_label}\nDevices Present: {devices_present}\nRemarks: {remarks}\nIn Use by: {in_use_by}\n\n")

        # Display SSH command for first result
        first_rpi_label = results[0][2]  # Assuming Rpi Label is at index 2
        ssh_command = f"ssh -L {first_rpi_label}:10.242.59.177:{first_rpi_label} BR09@orcus"
        pyperclip.copy(ssh_command)
        ssh_command_label.config(text=ssh_command)
    else:
        messagebox.showerror("Error", "No matching data found")

    conn.close()

def show_more_details():
    device_string = entry.get()
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()
    query = 'SELECT * FROM CRE_CRE_devices_Tracker_CSV WHERE "Devices Present" LIKE ?'
    cursor.execute(query, ('%' + device_string + '%',))
    results = cursor.fetchall()
    
    if results:
        details_window = tk.Toplevel(root)
        details_window.title("More Details")
        details_window.geometry("600x400")

        details_text = scrolledtext.ScrolledText(details_window, wrap=tk.WORD)
        details_text.pack(expand=True, fill='both')

        column_names = [desc[0] for desc in cursor.description]

        for result in results:
            details_text.insert(tk.END, "Row:\n")
            for col_name, value in zip(column_names, result):
                details_text.insert(tk.END, f"{col_name}: {value}\n")
            details_text.insert(tk.END, "\n")

    else:
        messagebox.showerror("Error", "No matching data found")

    conn.close()

# Create main window
root = tk.Tk()
root.title("Device Query Application")
root.geometry("500x500")

# UI Layout
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter Device String:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry = tk.Entry(frame, width=40, font=("Arial", 12))
entry.grid(row=0, column=1, padx=5, pady=5)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Filter", font=("Arial", 12), command=filter_data).grid(row=0, column=0, padx=10, pady=5)
tk.Button(btn_frame, text="More Details", font=("Arial", 12), command=show_more_details).grid(row=0, column=1, padx=10, pady=5)

# Output Box
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Arial", 12))
output_box.pack(expand=True, fill='both', padx=10, pady=5)

# SSH Command Label
ssh_command_label = tk.Label(root, text="", fg="blue", font=("Arial", 12, "bold"))
ssh_command_label.pack(pady=5)

# Run Application
root.mainloop()
