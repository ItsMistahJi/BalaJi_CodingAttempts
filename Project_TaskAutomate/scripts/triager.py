import re

def triage_logs(file_path):
    with open(file_path, 'r') as log_file:
        logs = log_file.readlines()

    error_logs = [line for line in logs if re.search(r'(ERROR|CRITICAL)', line, re.IGNORECASE)]
    
    print(f"Found {len(error_logs)} critical issues:")
    for log in error_logs:
        print(log.strip())