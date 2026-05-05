# planner.py

def create_plan(intent, user_input):
    text = user_input.lower()

    if "state lock" in text:
        return [
            "identify_issue",
            "unlock_state",
            "confirm_resolution"
        ]

    if "policy" in text:
        return [
            "identify_policy_issue",
            "fetch_policy_details",
            "suggest_fix"
        ]

    if "cost" in text:
        return [
            "analyze_resources",
            "identify_waste",
            "suggest_optimization"
        ]

    return ["analyze_query"]