# agent.py
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import time
from _phase9.monitoring.logger import log_info, log_error

from _phase9.memory.conversation_memory import ConversationMemory
from _phase9.planner.planner import create_plan

memory = ConversationMemory()
MAX_MEMORY = 5

from _phase9.feedback.feedback_store import FeedbackStore
from _phase9.adaptation.adaptive_logic import adjust_behavior

feedback_store = FeedbackStore()

from _phase9.intent_router import classify_intent
from _phase9.responders.failure import handle_failure
from _phase9.responders.policy import handle_policy
from _phase9.responders.cost import handle_cost
from _phase9.responders.fallback import handle_fallback
from _phase9.autos_logger import log_interaction, sanitize

from _phase9.tools.tool_registry import TOOLS

# Keep Phase 3 style prompt system
from _phase9.llm.client import call_llm, load_prompt, safe_parse

# FAISS retrieval
from _phase9.rag.faiss_store import semantic_search

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

    text = user_input.lower()

    # -----------------------------------------
    # GUARDRAILS
    # -----------------------------------------
    if "delete" in text and "production" in text:
        return {
            "status": "blocked",
            "reason": "Destructive production actions require approval"
        }, None

    # -----------------------------------------
    # RETRIEVAL
    # -----------------------------------------
    retrieved_docs = semantic_search(user_input)

    if not retrieved_docs:
        return {
            "status": "escalation",
            "reason": "No relevant knowledge found"
        }, None

    context = "\n".join(retrieved_docs)

    # -----------------------------------------
    # MEMORY CONTEXT
    # -----------------------------------------
    memory_context = memory.get_context()

    # -----------------------------------------
    # MEMORY-BASED FOLLOW-UP HANDLING
    # -----------------------------------------
    if memory_context:
        last_interaction = memory_context[-1]
        last_response = last_interaction.get("response", {})

        # Retry logic
        if "retry" in user_input.lower():
            if last_response.get("status") == "resolved":
                return {
                    "status": "resolved",
                    "message": "Yes, the previous issue has been resolved. You can safely retry the Terraform run.",
                    "based_on": "memory"
                }, None

            else:
                return {
                    "status": "warning",
                    "message": "The previous issue may not be fully resolved. Please verify before retrying.",
                    "based_on": "memory"
                }, None
    # -----------------------------------------
    # PLANNING
    # -----------------------------------------
    plan = create_plan(intent, user_input)

    print(f"[DEBUG] Plan: {plan}")
    print(f"[DEBUG] Memory: {memory_context}")

    # -----------------------------------------
    # FEEDBACK-BASED ADAPTATION
    # -----------------------------------------
    feedback_stats = feedback_store.get_feedback(user_input)
    adaptation = adjust_behavior(user_input, feedback_stats)

    print(f"[DEBUG] Feedback stats: {feedback_stats}")
    print(f"[DEBUG] Adaptation: {adaptation}")

    # -----------------------------------------
    # TOOL SELECTION
    # -----------------------------------------
    if adaptation["action"] == "avoid_tool":
        tool_name = None
    else:
        tool_name = select_tool(intent, user_input)

    print(f"[DEBUG] Tool selected: {tool_name}")

    tool_output = None

    if tool_name:

        if tool_name == "unlock_state":
            params = {"workspace": "dev"}

        elif tool_name == "get_run_status":
            params = {"run_id": "123"}

        elif tool_name == "get_policy":
            params = {}

        else:
            params = {}

        tool_output = execute_tool(tool_name, params)
        print(f"[DEBUG] Tool output: {tool_output}")

        # Accept ANY valid tool output
        if isinstance(tool_output, dict) and not tool_output.get("error"):
            return {
                "status": "resolved",
                "message": f"Tool '{tool_name}' executed successfully",
                "data": tool_output,
                "plan": plan
            }, None

        if isinstance(tool_output, dict) and tool_output.get("error"):
            return {
                "status": "error",
                "reason": tool_output["error"]
            }, None

        context += f"\nTool Output: {tool_output}"

    # -----------------------------------------
    # LLM REASONING (NOW WITH MEMORY + PLAN)
    # -----------------------------------------
    template = load_prompt(PROMPT_VERSION)


    trace = {
        "intent": intent,
        "plan": plan,
        "tool_used": tool_name,
        "feedback": feedback_stats,
    }
    log_info(f"Trace: {trace}")

    prompt = template.format(
        query=user_input,
        intent=intent,
        context=context,
        memory=memory_context,
        plan=plan
    )
    try:
        raw_response = call_llm(prompt)
        parsed_response = safe_parse(raw_response)
    except Exception as e:
        return {
            "status": "error",
            "reason": "LLM failure",
            "details": str(e)
        }, None

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
    try:
        if tool_name not in TOOLS:
            return {"error": "Invalid tool"}

        tool = TOOLS[tool_name]["function"]
        return tool(**params)

    except Exception as e:
        return {
            "error": "Tool execution failed",
            "details": str(e)
        }


# -----------------------------------------
# MAIN AGENT LOOP
# -----------------------------------------

def run_agent():
    print("AUTO-S Agent (Phase 9 - Safety, Evaluation & Governance)\nType 'exit' or 'reset'\n")

    while True:
        user_input = input("User: ")
        log_info(f"Query: {sanitize(user_input)}")

        if user_input.lower() == "exit":
            print("Exiting...")
            break

        if user_input.lower() == "reset":
            memory.reset()
            print("Memory cleared.\n")
            continue

        intent = classify_intent(user_input)

        print(f"[DEBUG] Intent: {intent}")
        print(f"[DEBUG] Prompt Version: {PROMPT_VERSION}")

        start_time = time.time()
        try:

            parsed, raw = route_llm_with_rag(intent, user_input)
            latency = round(time.time() - start_time, 3)
            log_info(f"Query: {user_input}")
            log_info(f"Intent: {intent}")
            log_info(f"Latency: {latency}s")
            log_info(f"Response: {parsed}")

        except Exception as e:
            log_error(f"Error: {str(e)}")
            print("Agent encountered an error. Please try again.")
            continue

        # -----------------------------------------
        # STORE MEMORY
        # -----------------------------------------
        memory.add(user_input, parsed)

        # RETENTION CONTROL
        if len(memory.history) > MAX_MEMORY:
            memory.history.pop(0)

        # -----------------------------------------
        # RESPONSE HANDLING
        # -----------------------------------------
        if parsed.get("status") in ["error"]:
            response = route_rule_based(intent, user_input)
            print(f"Agent (fallback): {response}\n")

        elif parsed.get("status") == "escalation":
            print(f"Agent (escalation): {parsed}\n")

        else:
            print(f"Agent: {parsed}\n")

    # -----------------------------------------
    # FEEDBACK COLLECTION
    # -----------------------------------------
    feedback = input("Was this helpful? (good/bad/skip): ").strip().lower()

    if feedback in ["good", "bad"]:
        feedback_store.add_feedback(user_input, feedback)


# -----------------------------------------
# ENTRY POINT
# -----------------------------------------
if __name__ == "__main__":
    run_agent()