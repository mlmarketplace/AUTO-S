# adaptive_logic.py

def adjust_behavior(query, feedback_stats):
    """
    Adjust agent behavior based on past feedback
    """

    good = feedback_stats.get("good", 0)
    bad = feedback_stats.get("bad", 0)

    # If bad feedback dominates → change strategy
    if bad > good:
        return {
            "mode": "conservative",
            "action": "avoid_tool",
            "reason": "Previous responses were not helpful"
        }

    # If good feedback dominates → keep current approach
    if good >= bad and good > 0:
        return {
            "mode": "normal",
            "action": "use_tool",
            "reason": "Previous responses were helpful"
        }

    # Default
    return {
        "mode": "default",
        "action": "standard_flow"
    }