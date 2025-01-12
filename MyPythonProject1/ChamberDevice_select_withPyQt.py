import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QLabel

# Hardcoded file path
EXCEL_FILE_PATH = r"C:\Users\BRU09\Downloads\CRE-CRE_devices_Tracker.xlsx"

# Initialize the dataframe globally
df = None

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Chamber Device Selector'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.load_button = QPushButton('Load Excel File', self)
        self.load_button.clicked.connect(self.load_excel)
        layout.addWidget(self.load_button)

        self.column_dropdown = QComboBox(self)
        layout.addWidget(self.column_dropdown)

        self.filter_entry = QLineEdit(self)
        self.filter_entry.setPlaceholderText('Enter filter value')
        layout.addWidget(self.filter_entry)

        self.filter_button = QPushButton('Filter Data', self)
        self.filter_button.clicked.connect(self.filter_data)
        layout.addWidget(self.filter_button)

        self.result_label = QLabel('', self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def load_excel(self):
        global df
        try:
            df = pd.read_excel(EXCEL_FILE_PATH)
            self.column_dropdown.addItems(df.columns)
            QMessageBox.information(self, "Success", f"File '{EXCEL_FILE_PATH}' loaded successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")

    def filter_data(self):
        selected_column = self.column_dropdown.currentText()
        filter_value = self.filter_entry.text()
        if not selected_column or not filter_value:
            QMessageBox.critical(self, "Error", "Please select a column and enter a filter value.")
            return

        try:
            filtered_df = df[df[selected_column].astype(str).str.contains(filter_value, na=False)]
            self.result_label.setText(f"Filtered {len(filtered_df)} rows.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to filter data: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())