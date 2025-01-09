import re
import tarfile
import tkinter as tk
from tkinter import filedialog, messagebox

# Define the files to be triaged for each category
CATEGORY_FILES = {
    "TelcoVoiceManager": ["TELCOVOICEMANAGERLog", "TELCOVOICEIFACEMGRLog", "VOICELog"],
    "IDM": ["InterDeviceManager", "systemd_processRestart", "GatewayManagerLog"],
    "MESH": ["MeshAgentLog", "MeshServiceLog", "MeshBlackbox"]
}

def triage_logs():
    # Create a Tkinter root window (it will not be shown)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select a file
    file_path = filedialog.askopenfilename(title="Select a log file, tar file, or tgz file", filetypes=[("Text files", "*.txt"), ("Tar files", "*.tar"), ("TGZ files", "*.tgz"), ("All files", "*.*")])
    
    if not file_path:
        print("No file selected.")
        return

    if file_path.endswith(('.tar', '.tgz')):
        # Create a new Tkinter window to select a category
        category_window = tk.Tk()
        category_window.title("Select a Category")

        selected_category = tk.StringVar(category_window)
        selected_category.set("TelcoVoiceManager")  # Set default value

        tk.Label(category_window, text="Select a category:").pack()
        tk.OptionMenu(category_window, selected_category, "TelcoVoiceManager", "IDM", "MESH").pack()

        def on_category_select():
            category_window.destroy()
            category = selected_category.get()
            files_to_check = CATEGORY_FILES[category]
            process_tar_file(file_path, files_to_check)

        tk.Button(category_window, text="Select", command=on_category_select).pack()
        category_window.mainloop()
    else:
        with open(file_path, 'r') as log_file:
            logs = log_file.readlines()
            process_logs(logs)

def process_tar_file(file_path, files_to_check):
    mode = 'r:gz' if file_path.endswith('.tgz') else 'r'
    with tarfile.open(file_path, mode) as tar:
        members = tar.getmembers()
        filtered_members = [member for member in members if any(file in member.name for file in files_to_check)]

        if not filtered_members:
            messagebox.showinfo("No Matches", "No matching files found in the tar archive.")
            return

        logs = []
        for member in filtered_members:
            with tar.extractfile(member) as log_file:
                logs.extend(log_file.read().decode('utf-8').splitlines())

        process_logs(logs, filtered_members)

def process_logs(logs, filtered_members=None):
    error_logs = [line for line in logs if re.search(r'(ERROR|CRITICAL)', line, re.IGNORECASE)]
    
    result_message = f"Found {len(error_logs)} critical issues."
    detailed_message = "\n".join(log.strip() for log in error_logs)
    
    # Create a new Tkinter window to show the results and provide an option to copy to clipboard
    result_window = tk.Tk()
    result_window.title("Triage Results")

    tk.Label(result_window, text=result_message, justify=tk.LEFT).pack()

    def copy_to_clipboard():
        result_window.clipboard_clear()
        result_window.clipboard_append(detailed_message)
        messagebox.showinfo("Clipboard", "Results copied to clipboard!")

    tk.Button(result_window, text="Copy to Clipboard", command=copy_to_clipboard).pack()
    tk.Button(result_window, text="Close", command=result_window.destroy).pack()

    result_window.mainloop()

if __name__ == "__main__":
    triage_logs()