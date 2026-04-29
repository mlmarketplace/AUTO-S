import os
from tools.log_parser import extract_error
from workflows.incident_debugging import diagnose_issue

def run_agent(user_query: str) -> str:
    """
    Main entry point for the agent
    """

    # Step 1: Get logs (for now, simulate)
    log_data = load_sample_logs()

    # Step 2: Extract error
    error = extract_error(log_data)

    # Step 3: Diagnose issue
    result = diagnose_issue(user_query, error)

    return result


def load_sample_logs():
    with open("data/logs/sample.log", "r") as f:
        return f.read()