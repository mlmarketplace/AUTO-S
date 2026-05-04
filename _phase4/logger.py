from datetime import datetime
import json

def log_interaction(user_input, response, intent, mode="rule"):
    with open("sample_logs.txt", "a") as f:
        f.write(f"{datetime.now()} | Intent: {intent} | Mode: {mode}\n")
        f.write(f"User: {user_input}\n")

        # Handle dict (LLM JSON) vs string (rule-based)
        if isinstance(response, dict):
            f.write(f"Agent: {json.dumps(response, indent=2)}\n\n")
        else:
            f.write(f"Agent: {response}\n\n")