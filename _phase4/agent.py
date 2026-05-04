# agent.py
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from router import classify_intent
from _phase4.responders.failure import handle_failure
from _phase4.responders.policy import handle_policy
from _phase4.responders.cost import handle_cost
from _phase4.responders.fallback import handle_fallback
from logger import log_interaction

# 🔥 Keep Phase 3 style prompt system
from _phase4.llm.client import call_llm, load_prompt, safe_parse

# 🔥 FAISS retrieval
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

    # 🔍 Retrieve context
    retrieved_docs = semantic_search(user_input)

    # ❌ No knowledge → escalate
    if not retrieved_docs:
        return {
            "status": "escalation",
            "intent": intent,
            "reason": "No relevant knowledge found"
        }, None

    context = "\n".join(retrieved_docs)

    # 🔥 Load prompt version (same as Phase 3)
    template = load_prompt(PROMPT_VERSION)

    # 🔥 Inject context into prompt
    prompt = template.format(
        query=user_input,
        intent=intent,
        context=context
    )

    raw_response = call_llm(prompt)

    parsed_response = safe_parse(raw_response)

    return parsed_response, raw_response


# -----------------------------------------
# MAIN AGENT LOOP
# -----------------------------------------
def run_agent():
    print("AUTO-S Agent (Phase 4 - RAG + Prompt Versioning)\nType 'exit' to quit\n")

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