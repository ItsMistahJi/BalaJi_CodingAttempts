import requests
import json

def lambda_handler(event, context):
    # Extract user input from Lex request
    user_query = event['currentIntent']['slots']['Query']
    
    # GitHub API call
    repo_url = "https://api.github.com/repos/<username>/<repo>/contents"
    response = requests.get(repo_url)

    # Check if response is valid JSON
    try:
        files = response.json()
    except json.JSONDecodeError:
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {"contentType": "PlainText", "content": "Invalid GitHub API response."}
            }
        }

    # Ensure 'files' is a list
    if not isinstance(files, list):
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {"contentType": "PlainText", "content": "Unexpected response format from GitHub API."}
            }
        }

    # Find relevant file and extract content
    relevant_file = next(
        (file for file in files if isinstance(file, dict) and 'name' in file and user_query.lower() in file['name'].lower()),
        None
    )
    
    if relevant_file:
        file_content = requests.get(relevant_file['download_url']).text
        explanation = f"The file contains:\n{file_content}\nExplanation: This code does XYZ."
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {"contentType": "PlainText", "content": explanation}
            }
        }
    
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Failed",
            "message": {"contentType": "PlainText", "content": f"No relevant code found for query '{user_query}'."}
        }
    }
