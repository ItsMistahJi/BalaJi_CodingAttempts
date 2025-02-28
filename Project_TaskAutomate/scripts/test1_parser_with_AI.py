import sys
import re
import tarfile
import zipfile
import os
import tempfile
import openai
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QFileDialog, QLabel, QLineEdit
)

def extract_logs_from_archive(archive_path):
    """
    Extracts text files from tar, zip archives and returns their contents as a string.
    """
    extracted_text = ""
    temp_dir = tempfile.mkdtemp()
    
    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    elif archive_path.endswith(".tar"):
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(temp_dir)
    
    # Read extracted text files
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    extracted_text += f.read() + "\n"
    
    return extracted_text

def parse_logs(log_content):
    """
    Parses log files and extracts ERROR and WARN level logs.
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

def refine_summary_and_description(log_content):
    """
    Uses OpenAI to refine the Summary and Description based on the log content.
    """
    prompt_summary = f"""Generate a concise summary based on the following logs:
    {log_content}
    """
    prompt_description = f"""Generate a detailed, structured description for a JIRA ticket based on the following logs:
    {log_content}
    """
    
    summary_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an AI assistant that summarizes logs."},
                  {"role": "user", "content": prompt_summary}]
    )
    
    description_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an AI assistant that creates structured descriptions from logs."},
                  {"role": "user", "content": prompt_description}]
    )
    
    return summary_response["choices"][0]["message"]["content"], description_response["choices"][0]["message"]["content"]

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
        self.refine_button = QPushButton("Refine Summary & Description", self)
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.refine_button)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

        self.browse_button.clicked.connect(self.load_log_file)
        self.search_button.clicked.connect(self.search_logs)
        self.refine_button.clicked.connect(self.refine_logs)

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
        
    def refine_logs(self):
        """
        Uses OpenAI to refine Summary and Description based on the logs.
        """
        if self.log_content:
            summary, description = refine_summary_and_description(self.log_content)
            self.result_area.setText(f"Summary:\n{summary}\n\nDescription:\n{description}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogParserUI()
    window.show()
    sys.exit(app.exec_())
