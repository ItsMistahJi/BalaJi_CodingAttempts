import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Function to load Excel file
import io
import requests

# SharePoint file URL (replace with your file's URL)
SHAREPOINT_FILE_URL = "https://skyglobal-my.sharepoint.com/:x:/r/personal/balaji_rameshbabu_sky_uk/Documents/CRE-CRE_devices_Tracker.xlsx?d=w45cfbb8773014f79bdf42976638caab0&csf=1&web=1&e=6PNx73"

def load_excel():
    global df
    try:
        # Get the file content from SharePoint
        response = requests.get(SHAREPOINT_FILE_URL)
        response.raise_for_status()
        file_bytes = io.BytesIO(response.content)

        # Load the Excel file into a DataFrame
        df = pd.read_excel(file_bytes)
        column_dropdown["values"] = list(df.columns)  # Update column dropdown
        messagebox.showinfo("Success", "File loaded successfully from SharePoint!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file from SharePoint: {e}")

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

import xlwings as xw

def run_tool():
    # Get the active workbook and sheet
    wb = xw.Book.caller()
    sheet = wb.sheets.active

    # Call the load_excel function to load the file
    load_excel()

    # Example: Update Excel with DataFrame column headers
    sheet.range("A1").value = ["Filtered Results"]
    sheet.range("A2").value = list(df.columns)

