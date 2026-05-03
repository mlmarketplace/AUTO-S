def handle_failure(user_input: str) -> str:
    if "state lock" in user_input.lower():
        return "Detected possible state lock issue. Suggested fix: unlock_state."
    return "Terraform run failure detected. Please check logs and retry."