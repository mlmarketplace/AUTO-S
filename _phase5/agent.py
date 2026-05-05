# agent.py
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from router import classify_intent
from _phase4.responders.failure import handle_failure
from _phase4.responders.policy import handle_policy
from _phase4.responders.cost import handle_cost
from _phase4.responders.fallback import handle_fallback
from logger import log_interaction

from _phase5.tools.tool_registry import TOOLS

# Keep Phase 3 style prompt system
from _phase4.llm.client import call_llm, load_prompt, safe_parse

# FAISS retrieval
from _phase4.rag.faiss_store import semantic_search

USE_LLM = True
PROMPT_VERSION = "v3"   # switch between v1, v2, v3


# -----------------------------------------
# RULE-BASED ROUTING
# -----------------------------------------
def route_rule_based(intent, user_input):
    if intent == "failure":
        return handle_failure(user_input)
    elif intent == "policy":
        return handle_policy(user_input)
    elif intent == "cost":
        return handle_cost(user_input)
    else:
        return handle_fallback(user_input)


# -----------------------------------------
# LLM + RAG ROUTING (PHASE 4)
# -----------------------------------------
def route_llm_with_rag(intent, user_input):

    # -----------------------------------------
    # SAFETY: Guardrails (BLOCK dangerous actions early)
    # -----------------------------------------
    text = user_input.lower()

    if "delete" in text and "production" in text:
        return {
            "status": "blocked",
            "reason": "Destructive production actions require approval"
        }, None

    # -----------------------------------------
    # STEP 1: Retrieval
    # -----------------------------------------
    retrieved_docs = semantic_search(user_input)

    if not retrieved_docs:
        return {
            "status": "escalation",
            "intent": intent,
            "reason": "No relevant knowledge found"
        }, None

    context = "\n".join(retrieved_docs)

    print(f"[DEBUG] Context retrieved")

    # -----------------------------------------
    # STEP 2: Tool Selection
    # -----------------------------------------
    tool_name = select_tool(intent, user_input)
    print(f"[DEBUG] Tool selected: {tool_name}")

    tool_output = None
    tool_call_count = 0
    MAX_TOOL_CALLS = 2   #  LOOP PREVENTION

    # -----------------------------------------
    # STEP 3: Tool Execution (controlled)
    # -----------------------------------------
    if tool_name:

        if tool_call_count >= MAX_TOOL_CALLS:
            return {
                "status": "error",
                "reason": "Tool loop detected"
            }, None

        tool_call_count += 1

        # Param handling
        if tool_name == "unlock_state":
            params = {"workspace": "dev"}

        elif tool_name == "get_run_status":
            params = {"run_id": "123"}

        elif tool_name == "get_policy":
            params = {}  # keep consistent with tool signature

        else:
            params = {}

        # Execute tool
        tool_output = execute_tool(tool_name, params)

        print(f"[DEBUG] Tool output: {tool_output}")

        # -----------------------------------------
        # STEP 4: Tool Result Handling
        # -----------------------------------------
        if isinstance(tool_output, dict) and tool_output.get("status") == "success":
            return {
                "status": "resolved",
                "message": f"Tool '{tool_name}' executed successfully",
                "data": tool_output
            }, None

        if isinstance(tool_output, dict) and tool_output.get("error"):
            return {
                "status": "error",
                "reason": tool_output["error"]
            }, None

        # Inject into context for reasoning
        context += f"\n\nTool Output:\n{tool_output}"

    # -----------------------------------------
    # STEP 5: LLM Reasoning (only if needed)
    # -----------------------------------------
    template = load_prompt(PROMPT_VERSION)

    prompt = template.format(
        query=user_input,
        intent=intent,
        context=context
    )

    raw_response = call_llm(prompt)
    parsed_response = safe_parse(raw_response)

    return parsed_response, raw_response
# -----------------------------------------
# TOOLS
# -----------------------------------------
def select_tool(intent, user_input):
    text = user_input.lower()

    if "state lock" in text or "unlock" in text:
        return "unlock_state"

    if "run status" in text or "run failed" in text:
        return "get_run_status"

    if "policy" in text or "policy fail" in text:
        return "get_policy"

    return None

def execute_tool(tool_name, params):
    if tool_name not in TOOLS:
        return {"error": "Invalid tool"}

    tool = TOOLS[tool_name]["function"]

    try:
        return tool(**params)
    except Exception as e:
        return {"error": str(e)}


# -----------------------------------------
# MAIN AGENT LOOP
# -----------------------------------------
def run_agent():
    print("AUTO-S Agent (Phase 5 - RAG + MCP + Prompt Versioning)\nType 'exit' to quit\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            print("Exiting...")
            break

        intent = classify_intent(user_input)

        print(f"[DEBUG] Intent: {intent}")
        print(f"[DEBUG] Prompt Version: {PROMPT_VERSION}")

        if USE_LLM:
            parsed, raw = route_llm_with_rag(intent, user_input)

            # fallback if parsing fails
            if isinstance(parsed, dict) and parsed.get("status") == "error":
                response = route_rule_based(intent, user_input)
                print(f"Agent (fallback): {response}\n")
                log_interaction(user_input, response, intent, mode="fallback")

            elif isinstance(parsed, dict) and parsed.get("status") == "escalation":
                print(f"Agent (escalation): {parsed}\n")
                log_interaction(user_input, parsed, intent, mode="escalation")

            else:
                print(f"Agent (LLM + RAG): {parsed}\n")
                log_interaction(user_input, parsed, intent, mode=f"rag_{PROMPT_VERSION}")

        else:
            response = route_rule_based(intent, user_input)
            print(f"Agent: {response}\n")
            log_interaction(user_input, response, intent, mode="rule")




# -----------------------------------------
# ENTRY POINT
# -----------------------------------------
if __name__ == "__main__":
    run_agent()