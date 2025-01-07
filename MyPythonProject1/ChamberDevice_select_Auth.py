from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# SharePoint credentials and file info
SHAREPOINT_SITE_URL = "https://skyglobal-my.sharepoint.com/:x:/r/personal/balaji_rameshbabu_sky_uk/Documents/CRE-CRE_devices_Tracker.xlsm?d=wd90684dac1c14743b856cdf760684d3c&csf=1&web=1&e=GE2Xu0"
SHAREPOINT_DOC_LIBRARY = "Shared Documents"
FILE_NAME = "CRE-CRE_devices_Tracker.xlsm"
USERNAME = ""
PASSWORD = ""

# Function to download file from SharePoint
def download_file_from_sharepoint():
    try:
        ctx_auth = AuthenticationContext(SHAREPOINT_SITE_URL)
        if ctx_auth.acquire_token_for_user(USERNAME, PASSWORD):
            ctx = ClientContext(SHAREPOINT_SITE_URL, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()

            file_url = f"/sites/yoursite/{SHAREPOINT_DOC_LIBRARY}/{FILE_NAME}"
            local_file_path = FILE_NAME

            response = File.open_binary(ctx, file_url)
            with open(local_file_path, "wb") as local_file:
                local_file.write(response.content)

            return local_file_path
        else:
            raise Exception("Authentication failed")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download file: {e}")
        return None

# Function to load Excel file
def load_excel():
    global df
    file_path = download_file_from_sharepoint()
    if file_path:
        try:
            df = pd.read_excel(file_path)
            column_dropdown["values"] = list(df.columns)  # Update column dropdown
            messagebox.showinfo("Success", "File loaded successfully!")
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
