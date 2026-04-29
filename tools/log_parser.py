import re

def extract_error(log_text: str) -> str:
    """
    Extracts key Terraform error from logs
    """

    # Simple pattern (you can improve later)
    match = re.search(r"Error: (.+)", log_text)

    if match:
        return match.group(1)

    return "No clear error found"