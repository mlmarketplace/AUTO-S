def select_tool(intent, user_input):
    text = user_input.lower()

    if "state lock" in text:
        return "unlock_state"

    if "policy" in text:
        return "get_policy"

    return None


def execute_tool(tool_name, params):
    if tool_name == "unlock_state":
        return {"workspace": params["workspace"], "status": "unlocked"}

    if tool_name == "get_policy":
        return {"policy_violation": "missing_tags"}

    return {"error": "Unknown tool"}