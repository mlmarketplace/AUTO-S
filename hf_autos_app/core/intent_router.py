def classify_intent(text):
    text = text.lower()

    if "policy" in text:
        return "policy"
    if "fail" in text or "error" in text:
        return "failure"
    if "cost" in text:
        return "cost"

    return "unknown"