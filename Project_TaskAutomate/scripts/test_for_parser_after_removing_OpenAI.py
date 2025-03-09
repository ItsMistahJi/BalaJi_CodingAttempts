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
    Extracts text files from tar, zip archives and returns their contents as a string.
    Handles "0 file" types as well.
    """
    extracted_text = ""
    temp_dir = tempfile.mkdtemp()
    
    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    elif archive_path.endswith(".tar"):
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(temp_dir)
    
    # Read extracted text files including "0 file" types
    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    extracted_text += f.read() + "\n"
            except Exception as e:
                print(f"Skipping file {file_path}: {e}")
    
    return extracted_text

def parse_logs(log_content):
    """
    Parses log files and extracts ERROR level logs.
    """
    extracted_logs = []
    pattern = r"(\d{6}-\d{2}:\d{2}:\d{2}\.\d+) \[mod=(.*?), lvl=(ERROR)\] \[tid=(\d+)\] (.*)"
    
    for line in log_content.split("\n"):
        match = re.search(pattern, line)
        if match:
            timestamp, module, level, tid, message = match.groups()
            extracted_logs.append({
                "timestamp": timestamp,
                "module": module,
                "level": level,
                "tid": tid,
                "message": message
            })
    
    return extracted_logs

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
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter search term")
        self.search_button = QPushButton("Search", self)
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

        self.browse_button.clicked.connect(self.load_log_file)
        self.search_button.clicked.connect(self.search_logs)

        self.log_content = ""

    def load_log_file(self):
        """
        Opens a file dialog to select a log file and process it.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Log File", "", "All Files (*);;Text Files (*.txt);;Archives (*.tar *.zip)")
        
        if file_path:
            if file_path.endswith((".tar", ".zip")):
                self.log_content = extract_logs_from_archive(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    self.log_content = file.read()
            
            parsed_logs = parse_logs(self.log_content)
            formatted_logs = "\n".join(
                [f"Timestamp: {log['timestamp']}, Module: {log['module']}, Level: {log['level']}, TID: {log['tid']}, Message: {log['message']}"
                 for log in parsed_logs]
            )
            
            self.result_area.setText(formatted_logs if formatted_logs else "No logs found matching the pattern.")

    def search_logs(self):
        """
        Searches for a specific term in logs and displays the matching lines.
        """
        search_term = self.search_input.text()
        if search_term and self.log_content:
            matching_lines = "\n".join([line for line in self.log_content.split("\n") if search_term in line])
            self.result_area.setText(matching_lines if matching_lines else "No matches found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogParserUI()
    window.show()
    sys.exit(app.exec_())
