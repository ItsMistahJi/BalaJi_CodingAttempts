import sys
import openai
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox, QLineEdit
)

# Set your OpenAI API key
openai.api_key = "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"

def ai_agent(prompt):
    """AI agent using OpenAI to analyze C/C++ code and logs."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.5
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {e}"

class AIAssistantApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RDK AI Personal Assistant")
        self.setGeometry(300, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("RDK AI Personal Assistant", self)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # Input for prompt
        self.input_box = QTextEdit(self)
        self.input_box.setPlaceholderText("Enter your C/C++ code snippet or issue description here...")
        layout.addWidget(self.input_box)

        # Submit Button
        self.submit_button = QPushButton("Analyze", self)
        self.submit_button.clicked.connect(self.handle_analysis)
        layout.addWidget(self.submit_button)

        # Response Label
        self.response_label = QLabel("Response:", self)
        layout.addWidget(self.response_label)

        # Output Text Box
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)

        # Set layout
        self.setLayout(layout)

    def handle_analysis(self):
        user_input = self.input_box.toPlainText().strip()
        if not user_input:
            QMessageBox.warning(self, "Input Error", "Please enter a code snippet or issue description.")
            return

        self.response_label.setText("Analyzing... Please wait.")
        response = ai_agent(user_input)
        self.output_box.setText(response)
        self.response_label.setText("Response:")

def main():
    app = QApplication(sys.argv)
    window = AIAssistantApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
