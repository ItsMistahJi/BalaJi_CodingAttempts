import tkinter as tk
from tkinter import messagebox
import sqlite3
import pyperclip

# Connect to SQLite database
conn = sqlite3.connect(r'C:\Users\BRU09\Downloads\CRE-CRE_devices_Tracker_db_attempt1.db')
cursor = conn.cursor()

def filter_data():
    device_string = entry.get()
    query = f'SELECT * FROM CRE_CRE_devices_Tracker_CSV WHERE "Devices present" LIKE ?'
    cursor.execute(query, ('%' + device_string + '%',))
    result = cursor.fetchone()
    
    if result:
        rpi_label, devices_present, remarks, in_use_by = result[2], result[3], result[11], result[12]
        output_text.set(f"Rpi Label: {rpi_label}\nDevices Present: {devices_present}\nRemarks: {remarks}\nIn Use by: {in_use_by}")
        
        ssh_command = f"ssh -L {rpi_label}:10.242.59.177:{rpi_label} BR09@orcus"
        pyperclip.copy(ssh_command)
        ssh_command_text.set(ssh_command)
    else:
        messagebox.showerror("Error", "No matching data found")

def show_more_details():
    # Implement the logic to show more details
    pass

# Create main window
root = tk.Tk()
root.title("Device Query Application")
root.geometry("400x300")

# Input field
tk.Label(root, text="Enter Device String:").pack()
entry = tk.Entry(root)
entry.pack()

# Filter button
tk.Button(root, text="Filter", command=filter_data).pack()

# Output box
output_text = tk.StringVar()
tk.Label(root, textvariable=output_text, justify='left').pack()

# SSH command display
ssh_command_text = tk.StringVar()
tk.Label(root, textvariable=ssh_command_text, fg="blue").pack()

# More details button
tk.Button(root, text="More Details", command=show_more_details).pack()

# Run the application
root.mainloop()