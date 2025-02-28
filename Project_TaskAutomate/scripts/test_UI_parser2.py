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
    Extracts text files from tar, zip archives and returns their contents as a dictionary {filename: content}.
    """
    extracted_files = {}
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
            file_path = os.path.join(root, file)
            try:
                if os.path.getsize(file_path) == 0:
                    extracted_files[file] = "No logs found (empty file)."
                else:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        extracted_files[file] = f.read()
            except Exception as e:
                extracted_files[file] = f"Could not read file: {str(e)}"
    
    return extracted_files

def parse_logs(files_content, search_query=None):
    """
    Parses log files and extracts ERROR and WARN logs, or searches for a specific string.
    """
    extracted_logs = {}
    pattern = r"(\d{6}-\d{2}:\d{2}:\d{2}\.\d+) \[mod=(.*?), lvl=(ERROR)\] \[tid=(\d+)\] (.*)"
    
    for filename, content in files_content.items():
        if isinstance(content, str):  # Ensure content is a string before processing
            matches = []
            for line in content.split("\n"):
                if search_query and search_query in line:
                    matches.append(line)
                else:
                    match = re.search(pattern, line)
                    if match:
                        matches.append(line)
            extracted_logs[filename] = matches if matches else "No ERROR logs found."
    
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
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Enter search query (optional)")
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.search_box)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

        self.browse_button.clicked.connect(self.load_log_file)

    def load_log_file(self):
        """
        Opens a file dialog to select a log file and process it.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Log File", "", "All Files (*);;Text Files (*.txt);;Archives (*.tar *.zip)")
        
        if file_path:
            if file_path.endswith((".tar", ".zip")):
                files_content = extract_logs_from_archive(file_path)
            else:
                files_content = {}
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        files_content[os.path.basename(file_path)] = file.read()
                except Exception as e:
                    files_content[os.path.basename(file_path)] = f"Could not read file: {str(e)}"
            
            search_query = self.search_box.text().strip() or None
            parsed_logs = parse_logs(files_content, search_query)
            formatted_logs = "\n\n".join(
                [f"<b>File: {filename}</b>\n" + "\n".join(logs) if isinstance(logs, list) else f"<b>File: {filename}</b>\n{logs}"
                 for filename, logs in parsed_logs.items()]
            )
            
            self.result_area.setHtml(formatted_logs if formatted_logs else "No relevant logs found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogParserUI()
    window.show()
    sys.exit(app.exec_())
