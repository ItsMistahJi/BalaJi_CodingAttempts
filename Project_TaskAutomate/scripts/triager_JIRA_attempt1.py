import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QFileDialog, QLabel
)


class LogParserUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes the UI components.
        """
        self.setWindowTitle("AI Log Parser - JIRA Assistant")
        self.setGeometry(200, 200, 700, 500)  # Set window size

        # UI Elements
        self.label = QLabel("Select a log file to analyze:", self)
        self.browse_button = QPushButton("Browse File", self)
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)  # Make result text box read-only

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

        # Connect button click event
        self.browse_button.clicked.connect(self.load_log_file)

    def load_log_file(self):
        """
        Opens a file explorer dialog to select a log file and process it.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Log File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            parsed_logs = self.parse_logs(file_path)
            jira_suggestions = self.suggest_jira_fields(parsed_logs)
            self.display_results(jira_suggestions)

    def parse_logs(self, file_path):
        """
        Parses log files and extracts error messages with timestamps.
        """
        error_logs = []
        pattern = r"\[(.*?)\] (ERROR|WARNING): (.*)"  # Regex for timestamp and error messages
        
        with open(file_path, 'r') as file:
            for line in file:
                match = re.search(pattern, line)
                if match:
                    timestamp, log_type, message = match.groups()
                    error_logs.append({
                        "timestamp": timestamp,
                        "type": log_type,
                        "message": message
                    })
        
        return error_logs

    def suggest_jira_fields(self, logs):
        """
        Uses parsed logs to suggest JIRA ticket details.
        """
        if not logs:
            return "No issues detected in logs."

        first_issue = logs[0]  # Taking the first error for suggestion
        jira_fields = {
            "Summary": f"{first_issue['type']}: {first_issue['message']}",
            "Type": "Bug",
            "Resolution": "Unresolved",
            "Priority": "TBD by Dev Manager",
            "Component/s": "SOC",
            "Regression": "Yes" if "reboot" in first_issue["message"].lower() else "No",
            "Failure Type": "System Crash" if "kernel panic" in first_issue["message"].lower() else "Network Issue",
            "Description": f"*Defect Summary:*\n{first_issue['message']}\n\n"
                           f"*Timestamp:*\n{first_issue['timestamp']}\n\n"
                           f"*Logs:*\n{{noformat}} {first_issue['message']} {{noformat}}"
        }

        result_text = "\n".join(f"{key}: {value}" for key, value in jira_fields.items())
        return result_text

    def display_results(self, result_text):
        """
        Displays the parsed results in the text box.
        """
        self.result_area.setText(result_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogParserUI()
    window.show()
    sys.exit(app.exec())
