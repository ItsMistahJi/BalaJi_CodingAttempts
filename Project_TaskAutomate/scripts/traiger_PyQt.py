import re
import tarfile
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QMessageBox

# Define the files to be triaged for each category
CATEGORY_FILES = {
    "TelcoVoiceManager": ["TELCOVOICEMANAGERLog", "TELCOVOICEIFACEMGRLog", "VOICELog"],
    "IDM": ["InterDeviceManager", "systemd_processRestart", "GatewayManagerLog"],
    "MESH": ["MeshAgentLog", "MeshServiceLog", "MeshBlackbox"]
}

class TriageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Triage Logs')
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.showFileDialog()

    def showFileDialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a log file, tar file, or tgz file", "", "All Files (*);;Text Files (*.txt);;Tar Files (*.tar);;TGZ Files (*.tgz)", options=options)
        
        if file_path:
            if file_path.endswith(('.tar', '.tgz')):
                self.showCategoryDialog(file_path)
            else:
                with open(file_path, 'r') as log_file:
                    logs = log_file.readlines()
                    self.process_logs(logs)
        else:
            self.close()

    def showCategoryDialog(self, file_path):
        self.category_window = QWidget()
        self.category_window.setWindowTitle('Select a Category')
        self.category_layout = QVBoxLayout()
        self.category_window.setLayout(self.category_layout)

        self.category_label = QLabel('Select a category:')
        self.category_layout.addWidget(self.category_label)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["TelcoVoiceManager", "IDM", "MESH"])
        self.category_layout.addWidget(self.category_combo)

        self.select_button = QPushButton('Select')
        self.select_button.clicked.connect(lambda: self.on_category_select(file_path))
        self.category_layout.addWidget(self.select_button)

        self.category_window.show()

    def on_category_select(self, file_path):
        category = self.category_combo.currentText()
        files_to_check = CATEGORY_FILES[category]
        self.category_window.close()
        self.process_tar_file(file_path, files_to_check)

    def process_tar_file(self, file_path, files_to_check):
        mode = 'r:gz' if file_path.endswith('.tgz') else 'r'
        with tarfile.open(file_path, mode) as tar:
            members = tar.getmembers()
            filtered_members = [member for member in members if any(file in member.name for file in files_to_check)]

            if not filtered_members:
                QMessageBox.information(self, "No Matches", "No matching files found in the tar archive.")
                self.close()
                return

            logs = []
            for member in filtered_members:
                with tar.extractfile(member) as log_file:
                    logs.extend(log_file.read().decode('utf-8').splitlines())

            self.process_logs(logs)

    def process_logs(self, logs):
        error_logs = [line for line in logs if re.search(r'(ERROR|CRITICAL)', line, re.IGNORECASE)]
        
        result_message = f"Found {len(error_logs)} critical issues."
        detailed_message = "\n".join(log.strip() for log in error_logs)
        
        self.result_window = QWidget()
        self.result_window.setWindowTitle('Triage Results')
        self.result_layout = QVBoxLayout()
        self.result_window.setLayout(self.result_layout)

        self.result_label = QLabel(result_message)
        self.result_layout.addWidget(self.result_label)

        self.copy_button = QPushButton('Copy to Clipboard')
        self.copy_button.clicked.connect(lambda: self.copy_to_clipboard(detailed_message))
        self.result_layout.addWidget(self.copy_button)

        self.save_button = QPushButton('Save to File')
        self.save_button.clicked.connect(lambda: self.save_to_file(detailed_message))
        self.result_layout.addWidget(self.save_button)

        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close_window)
        self.result_layout.addWidget(self.close_button)

        self.result_window.show()

    def copy_to_clipboard(self, detailed_message):
        clipboard = QApplication.clipboard()
        clipboard.setText(detailed_message)
        QMessageBox.information(self, "Clipboard", "Results copied to clipboard!")

    def save_to_file(self, detailed_message):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Results to File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(detailed_message)
            QMessageBox.information(self, "File Saved", f"Results saved to {file_path}")

    def close_window(self):
        self.result_window.close()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TriageApp()
    sys.exit(app.exec_())