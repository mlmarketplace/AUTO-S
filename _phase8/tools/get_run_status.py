# tools/get_run_status.py
def get_run_status(run_id: str):
    # Dummy simulation
    print("Tool get run status")
    return {
        "run_id": run_id,
        "status": "failed",
        "error": "state lock"
    }