from datetime import datetime

def log_interaction(user_input, response, intent):
    with open("sample_logs.txt", "a") as f:
        f.write(f"{datetime.now()} | Intent: {intent}\n")
        f.write(f"User: {user_input}\n")
        f.write(f"Agent: {response}\n\n")