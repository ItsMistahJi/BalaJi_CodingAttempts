import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Hardcoded file path
EXCEL_FILE_PATH = r"C:\Users\BRU09\Downloads\CRE-CRE_devices_Tracker.xlsx"

# Initialize the dataframe globally
df = None

# Function to load Excel file
def load_excel():
    global df
    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
        column_dropdown["values"] = list(df.columns)  # Update column dropdown
        messagebox.showinfo("Success", f"File '{EXCEL_FILE_PATH}' loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")

# Function to filter data
def filter_data():
    selected_column = column_dropdown.get()
    filter_value = filter_entry.get()
    if not selected_column or not filter_value:
        messagebox.showerror("Error", "Please select a column and enter a filter value.")
        return

    try:
        filtered_df = df[df[selected_column].astype(str).str.contains(filter_value, case=False, na=False)]
        show_results(filtered_df)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to filter data: {e}")

# Function to display results
def show_results(filtered_df):
    result_window = tk.Toplevel()
    result_window.title("Filtered Results")

    table_frame = ttk.Frame(result_window)
    table_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(table_frame, columns=list(filtered_df.columns), show="headings")
    for col in filtered_df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for _, row in filtered_df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill="both", expand=True)

# Main Application
root = tk.Tk()
root.title("Excel Data Filter")

# Dropdown for column selection
column_dropdown_label = ttk.Label(root, text="Select Column:")
column_dropdown_label.pack()
column_dropdown = ttk.Combobox(root, state="readonly")
column_dropdown.pack(pady=5)

# Entry for filter value
filter_label = ttk.Label(root, text="Enter Filter Value:")
filter_label.pack()
filter_entry = ttk.Entry(root)
filter_entry.pack(pady=5)

# Filter Button
filter_button = ttk.Button(root, text="Filter Data", command=filter_data)
filter_button.pack(pady=10)

# Load the file on startup
load_excel()

root.mainloop()
