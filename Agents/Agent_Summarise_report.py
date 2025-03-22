import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QClipboard
from PyQt5.QtCore import Qt
import pyperclip
import openpyxl

class TaskTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Task Tracker Report Generator')
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("border-radius: 15px;")

        layout = QVBoxLayout()

        # Week Number Inputs
        self.week_label = QLabel('Week Number 1:')
        self.week_input1 = QLineEdit()
        layout.addWidget(self.week_label)
        layout.addWidget(self.week_input1)

        self.week_label2 = QLabel('Week Number 2:')
        self.week_input2 = QLineEdit()
        layout.addWidget(self.week_label2)
        layout.addWidget(self.week_input2)

        # Start Date Input
        self.start_date_label = QLabel('Start Date (dd/mm/yyyy):')
        self.start_date_input = QLineEdit()
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)

        # End Date Input
        self.end_date_label = QLabel('End Date (dd/mm/yyyy):')
        self.end_date_input = QLineEdit()
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_input)

        # Generate Report Button
        self.generate_button = QPushButton('Generate Report')
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px;")
        self.generate_button.clicked.connect(self.generate_report)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def generate_report(self):
        week_number1 = self.week_input1.text()
        week_number2 = self.week_input2.text()
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()

        if not week_number1 or not week_number2 or not start_date or not end_date:
            QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
            return

        try:
            # Use raw string for file path
            file_path = r'C:\Users\BRU09\Downloads\Task Tracker (1).xlsx'
            #file_path = r'C:\Users\BRU09\OneDrive - Sky\Documents\Personal\Appraisals_and_reports\Task Tracker.xlsx'
            workbook = openpyxl.load_workbook(file_path)

            # Update "Weekly_report" sheet
            weekly_report_sheet = workbook['Weekly_report']
            weekly_report_sheet['A2'] = week_number1
            weekly_report_sheet['A3'] = week_number2

            # Update "Wednesday_report" sheet
            wednesday_report_sheet = workbook['Wednesday_report']
            wednesday_report_sheet['B1'] = start_date
            wednesday_report_sheet['B2'] = end_date

            # Save the workbook to apply changes
            workbook.save(file_path)

            # Reload the workbook to ensure changes are applied
            workbook = openpyxl.load_workbook(file_path, data_only=True)

            # Load the "Report_to_Share" sheet
            report_to_share_sheet = workbook['Report_to_Share']
            report_output = report_to_share_sheet['A1'].value

            # Copy the summary report to the clipboard
            pyperclip.copy(report_output)
            QMessageBox.information(self, 'Success', 'Report generated and copied to clipboard.')

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskTrackerApp()
    ex.show()
    sys.exit(app.exec_())