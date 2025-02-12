import openai

# Set up your OpenAI API key
openai.api_key = "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"

def ai_agent(prompt):
    """Simple AI agent that uses OpenAI GPT to answer a question."""
    try:
        response = openai.ChatCompletion.create(
            model="tts-1",  # You can use "gpt-3.5-turbo" if you prefer
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.5  # Limit the length of the response
        )
        # Extract and return the response from the AI
        answer = response.choices[0].message['content']
        return answer.strip()
    except Exception as e:
        return f"Error: {e}"

# Main loop to interact with the AI agent
if __name__ == "__main__":
    print("Welcome to your AI Agent! (Type 'quit' to exit)")
    while True:
        user_input = input("\nAsk me anything: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        response = ai_agent(user_input)
        print(f"\nAI Agent: {response}")
