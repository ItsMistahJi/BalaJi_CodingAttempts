import sys
import pandas as pd
import re
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
from PyQt5.QtWidgets import QApplication, QFileDialog

# Define the regex pattern for log parsing
LOG_PATTERN = r"""
^(?P<timestamp>\d{6}-\d{2}:\d{2}:\d{2}\.\d+)\s+
\[mod=(?P<module>[^\]]+),\s+lvl=(?P<level>[^\]]+)\]\s+
\[tid=(?P<tid>\d+)\]\s+
(?P<function>[^\[]+)\[(?P<line>\d+)\]\s+
(?P<message>.+)
"""

# Function to parse logs
def parse_logs(file_path):
    log_regex = re.compile(LOG_PATTERN, re.VERBOSE)
    parsed_logs = []

    with open(file_path, 'r', errors='ignore') as log_file:
        for line in log_file:
            match = log_regex.match(line)
            if match:
                parsed_logs.append(match.groupdict())

    return pd.DataFrame(parsed_logs)

# Function to open file picker using PyQt5
def select_file():
    app = QApplication(sys.argv)
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("All Files (*)")  # Allow all file types

    if file_dialog.exec_():
        file_paths = file_dialog.selectedFiles()
        return file_paths[0] if file_paths else None

# Initially, load a default file or empty DataFrame
selected_file = select_file()
logs_df = parse_logs(selected_file) if selected_file else pd.DataFrame()

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Log File Dashboard"),
    
    html.Button("Select File", id="file-button", n_clicks=0),
    html.Div(id="selected-file", children=f"Selected file: {selected_file}" if selected_file else "No file selected"),
    
    dcc.Dropdown(
        id="level-dropdown",
        options=[{"label": level, "value": level} for level in logs_df["level"].unique()] if not logs_df.empty else [],
        placeholder="Select Log Level",
    ),
    
    dcc.Graph(id="bar-chart"),
    html.Div(id="log-details")
])

@app.callback(
    Output("selected-file", "children"),
    Output("level-dropdown", "options"),
    Output("bar-chart", "figure"),
    Output("log-details", "children"),
    Input("file-button", "n_clicks"),
    State("level-dropdown", "value"),
    prevent_initial_call=True
)
def update_dashboard(n_clicks, selected_level):
    global selected_file, logs_df  # Use global to store the selected file

    # Open file picker
    selected_file = select_file()
    if not selected_file:
        return "No file selected", [], {}, ""

    logs_df = parse_logs(selected_file)
    level_options = [{"label": level, "value": level} for level in logs_df["level"].unique()]

    # Filter logs by level
    filtered_logs = logs_df if not selected_level else logs_df[logs_df["level"] == selected_level]

    # Create bar chart
    fig = px.bar(
        filtered_logs["module"].value_counts(),
        x=filtered_logs["module"].value_counts().index,
        y=filtered_logs["module"].value_counts().values,
        labels={"x": "Module", "y": "Log Count"},
        title=f"Log Count by Module ({selected_level or 'All'})"
    )

    # Log details
    details = filtered_logs.to_html()

    return f"Selected file: {selected_file}", level_options, fig, details

if __name__ == "__main__":
    app.run_server(debug=True)
