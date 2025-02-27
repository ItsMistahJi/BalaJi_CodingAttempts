import sys
import re
import tarfile
import zipfile
import os
import tempfile
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QFileDialog, QLabel, QLineEdit
)

def extract_logs_from_archive(archive_path):
    """
    Extracts text files from tar, zip archives and returns their contents as a dictionary.
    """
    extracted_logs = {}
    temp_dir = tempfile.mkdtemp()
    
    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    elif archive_path.endswith(".tar"):
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(temp_dir)
    
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                extracted_logs[file] = read_file(file_path)
    
    return extracted_logs

def read_file(file_path):
    """Reads a file with error handling for encoding issues."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.readlines()
    except Exception as e:
        return [f"Error reading file {file_path}: {str(e)}"]

def parse_logs(file_contents):
    """
    Extracts only ERROR and WARN level logs from the log contents and organizes them by filename.
    """
    extracted_logs = {}
    pattern = r"(\d{6}-\d{2}:\d{2}:\d{2}\.\d+) \[mod=(.*?), lvl=(ERROR|WARN)\] \[tid=(\d+)\] (.*)"
    
    for filename, content in file_contents.items():
        logs = []
        for line in content:
            match = re.search(pattern, line)
            if match:
                timestamp, module, level, tid, message = match.groups()
                logs.append(f"[{level}] {timestamp} - Module: {module}, TID: {tid}, Message: {message}")
        
        extracted_logs[filename] = logs if logs else ["No ERROR or WARN logs found."]
    
    return extracted_logs

def search_logs(file_contents, search_string):
    """Searches for a user-provided string in all log files."""
    search_results = {}
    for filename, content in file_contents.items():
        matches = [line.strip() for line in content if search_string.lower() in line.lower()]
        search_results[filename] = matches if matches else ["No matching entries found."]
    return search_results

class LogParserUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes the UI components.
        """
        self.setWindowTitle("AI Log Parser - JIRA Assistant")
        self.setGeometry(200, 200, 800, 600)

        self.label = QLabel("Select a log file (txt, tar, zip) to analyze:", self)
        self.browse_button = QPushButton("Browse File", self)
        self.search_label = QLabel("Enter a string to search in logs:", self)
        self.search_input = QLineEdit(self)
        self.search_button = QPushButton("Search", self)
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

        self.browse_button.clicked.connect(self.load_log_file)
        self.search_button.clicked.connect(self.search_in_logs)

    def load_log_file(self):
        """
        Opens a file dialog to select a log file and process it.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Log File", "", "All Files (*);;Text Files (*.txt);;Archives (*.tar *.zip)")
        
        if file_path:
            if file_path.endswith((".tar", ".zip")):
                log_contents = extract_logs_from_archive(file_path)
            else:
                log_contents = {os.path.basename(file_path): read_file(file_path)}
            
            parsed_logs = parse_logs(log_contents)
            formatted_logs = "\n".join(
                [f"{filename}:\n" + "\n".join(logs) for filename, logs in parsed_logs.items()]
            )
            
            self.result_area.setText(formatted_logs if formatted_logs else "No logs found matching the pattern.")
            self.log_contents = log_contents  # Store log contents for searching

    def search_in_logs(self):
        """Searches for user-provided string in loaded log files."""
        search_string = self.search_input.text().strip()
        if not hasattr(self, 'log_contents') or not search_string:
            self.result_area.setText("No logs loaded or search term empty.")
            return
        
        search_results = search_logs(self.log_contents, search_string)
        formatted_results = "\n".join(
            [f"{filename}:\n" + "\n".join(results) for filename, results in search_results.items()]
        )
        
        self.result_area.setText(formatted_results if formatted_results else "No matches found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogParserUI()
    window.show()
    sys.exit(app.exec_())
