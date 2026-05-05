# tools/unlock_state.py
def unlock_state(workspace: str):
    print("Tool unlock state")
    return {
        "workspace": workspace,
        "action": "unlock",
        "status": "success"
    }