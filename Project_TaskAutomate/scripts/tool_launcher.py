import subprocess
import json

def open_tools(config_file):
    with open(config_file, 'r') as file:
        tools = json.load(file)
    
    for tool_name, tool_path in tools.items():
        print(f"Opening {tool_name}...")
        subprocess.Popen([tool_path])

if __name__ == "__main__":
    open_tools('config/tools.json')
