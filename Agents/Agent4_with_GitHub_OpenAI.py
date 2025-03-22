import openai
import github3
import requests

# Set your OpenAI API key
openai.api_key = "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"

def ai_agent(prompt):
    """AI agent using OpenAI to analyze C/C++ code and logs."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.5
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {e}"


def fetch_github_file(repo_url, file_path, github_token):
    """Fetch the content of a file from a GitHub repository."""
    try:
        owner, repo_name = repo_url.rstrip('/').split("/")[-2:]
        
        # Authenticate with GitHub API
        gh = github3.login(token=github_token)
        repo = gh.repository(owner, repo_name)
        
        # Get file contents
        contents = repo.file_contents(file_path)
        return contents.decoded.decode('utf-8')

    except Exception as e:
        return f"Error fetching file from GitHub: {e}"

def analyze_code_from_github(repo_url, file_path, token):
    """Analyze a C/C++ code file from a GitHub repository."""
    code = fetch_github_file(repo_url, file_path, token)
    if "Error" in code:
        return code
    prompt = f"You are an AI assistant helping to analyze and debug RDK open-source C/C++ code.\n\nHere is the code from {file_path}:\n{code}\n\nPlease analyze the code, explain what it does, and suggest possible improvements or fixes."
    return ai_agent(prompt)

def analyze_log(log_content):
    """Analyze logs and suggest possible solutions."""
    prompt = f"You are an AI assistant analyzing logs from an RDK C/C++ project.\n\nHere are the logs:\n{log_content}\n\nPlease identify possible issues and suggest solutions."
    return ai_agent(prompt)

def main():
    print("Welcome to the Enhanced RDK AI Agent! (Type 'quit' to exit)")
    while True:
        print("\nOptions:")
        print("1. Analyze a C/C++ code file from GitHub")
        print("2. Analyze real-time logs")
        print("Type 'quit' to exit.")
        choice = input("Choose an option (1 or 2): ").strip()

        if choice.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        elif choice == "1":
            repo_url = input("\nEnter the GitHub repository URL (e.g., https://github.com/RDKCentral/rdkservices): ").strip()
            file_path = input("Enter the file path in the repository (e.g., src/main.cpp): ").strip()
            response = analyze_code_from_github(repo_url, file_path, "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")
            print(f"\nAI Agent Response:\n{response}")
        elif choice == "2":
            log_content = input("\nPaste your log content:\n")
            response = analyze_log(log_content)
            print(f"\nAI Agent Response:\n{response}")
        else:
            print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
