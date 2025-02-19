import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3
import pyperclip

# Connect to SQLite database
conn = sqlite3.connect(r'C:\Users\BRU09\Downloads\CRE-CRE_devices_Tracker_db_attempt1.db')
cursor = conn.cursor()

def filter_data():
    device_string = entry.get()
    query = f'SELECT * FROM CRE_CRE_devices_Tracker_CSV WHERE "Devices present" LIKE ?'
    cursor.execute(query, ('%' + device_string + '%',))
    results = cursor.fetchall()
    
    if results:
        output_text.set("")
        for result in results:
            rpi_label, devices_present, remarks, in_use_by = result[2], result[3], result[11], result[12]
            output_text.set(output_text.get() + f"Rpi Label: {rpi_label}\nDevices Present: {devices_present}\nRemarks: {remarks}\nIn Use by: {in_use_by}\n\n")
        
        # Display SSH command for the first result
        first_rpi_label = results[0][0]
        ssh_command = f"ssh -L {first_rpi_label}:10.242.59.177:{first_rpi_label} BR09@orcus"
        pyperclip.copy(ssh_command)
        ssh_command_text.set(ssh_command)
    else:
        messagebox.showerror("Error", "No matching data found")

def show_more_details():
    device_string = entry.get()
    query = f'SELECT * FROM CRE_CRE_devices_Tracker_CSV WHERE "Devices present" LIKE ?'
    cursor.execute(query, ('%' + device_string + '%',))
    results = cursor.fetchall()
    
    if results:
        details_window = tk.Toplevel(root)
        details_window.title("More Details")
        details_window.geometry("600x400")
        
        details_text = scrolledtext.ScrolledText(details_window, wrap=tk.WORD)
        details_text.pack(expand=True, fill='both')
        
        # Fetch column names
        column_names = [description[0] for description in cursor.description]
        
        for result in results:
            details_text.insert(tk.END, "Row:\n")
            for col_name, value in zip(column_names, result):
                details_text.insert(tk.END, f"{col_name}: {value}\n")
            details_text.insert(tk.END, "\n")
    else:
        messagebox.showerror("Error", "No matching data found")

def show_more_details():
    # Implement the logic to show more details
    pass

# Create main window
# Create main window
root = tk.Tk()
root.title("Device Query Application")
root.geometry("500x400")

# Input field
tk.Label(root, text="Enter Device String:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Filter button
tk.Button(root, text="Filter", command=filter_data).pack(pady=5)

# Output box
output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, justify='left', anchor='w')
output_label.pack(pady=5, fill='both', expand=True)

# SSH command display
ssh_command_text = tk.StringVar()
ssh_command_label = tk.Label(root, textvariable=ssh_command_text, fg="blue")
ssh_command_label.pack(pady=5)

# More details button
tk.Button(root, text="More Details", command=show_more_details).pack(pady=5)

# Run the application
root.mainloop()