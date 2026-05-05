# tools/tool_registry.py

from _phase5.tools.get_run_status import get_run_status
from _phase5.tools.unlock_state import unlock_state
from _phase5.tools.get_policy import get_policy

TOOLS = {
    "get_run_status": {
        "function": get_run_status,
        "description": "Fetch Terraform run status using run ID",
        "args": ["run_id"]
    },
    "unlock_state": {
        "function": unlock_state,
        "description": "Unlock Terraform state for a workspace",
        "args": ["workspace"]
    },
    "get_policy": {
        "function": get_policy,
        "description": "Fetch policy violation details"
    }
}