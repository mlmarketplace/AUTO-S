def classify_intent(user_input: str) -> str:
    text = user_input.lower()

    if "fail" in text or "error" in text:
        return "failure"
    elif "policy" in text:
        return "policy"
    elif "cost" in text or "expensive" in text:
        return "cost"
    else:
        return "unknown"