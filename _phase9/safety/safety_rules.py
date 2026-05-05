def enforce_safety(user_input):
    text = user_input.lower()

    # Destructive actions
    if "delete" in text and "production" in text:
        return {
            "status": "blocked",
            "reason": "Production destructive actions require approval"
        }

    # Sensitive data (basic PII guard)
    if "password" in text or "secret" in text:
        return {
            "status": "refusal",
            "reason": "Sensitive information cannot be processed"
        }

    return None