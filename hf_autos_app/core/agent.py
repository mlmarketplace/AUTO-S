import time

from core.intent_router import classify_intent
from core.tools import execute_tool, select_tool
from rag.faiss_store import semantic_search

# -----------------------------------------
# CONFIG
# -----------------------------------------
USE_RAG = True


# -----------------------------------------
# MAIN AGENT FUNCTION
# -----------------------------------------
def route_llm_with_rag(intent, user_input):
    """
    Core agent logic:
    1. Retrieve context (RAG)
    2. Decide tool usage
    3. Execute tool (if needed)
    4. Return structured response
    """

    try:
        # -----------------------------------------
        # STEP 1: RETRIEVAL
        # -----------------------------------------
        context = []
        if USE_RAG:
            context = semantic_search(user_input)

        if not context:
            return {
                "status": "escalation",
                "reason": "No relevant knowledge found"
            }, None

        context_text = "\n".join(context)

        # -----------------------------------------
        # STEP 2: TOOL SELECTION
        # -----------------------------------------
        tool_name = select_tool(intent, user_input)
        tool_output = None

        # -----------------------------------------
        # STEP 3: TOOL EXECUTION
        # -----------------------------------------
        if tool_name:
            if tool_name == "unlock_state":
                params = {"workspace": "dev"}

            elif tool_name == "get_policy":
                params = {"policy_id": "default"}

            else:
                params = {}

            tool_output = execute_tool(tool_name, params)

            return {
                "status": "resolved",
                "message": f"Tool '{tool_name}' executed successfully",
                "data": tool_output
            }, None

        # -----------------------------------------
        # STEP 4: RAG RESPONSE (NO TOOL)
        # -----------------------------------------
        return {
            "status": "resolved",
            "message": "Answer generated using knowledge base",
            "data": context_text[:500]
        }, None

    except Exception as e:
        return {
            "status": "error",
            "reason": "Agent execution failed",
            "details": str(e)
        }, None