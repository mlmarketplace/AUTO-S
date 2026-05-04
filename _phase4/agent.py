# agent.py

from router import classify_intent
from responders.failure import handle_failure
from responders.policy import handle_policy
from responders.cost import handle_cost
from responders.fallback import handle_fallback
from logger import log_interaction


from _phase4.llm.client import call_llm, load_prompt, safe_parse

from rag.embedding_store import search

USE_LLM = True
PROMPT_VERSION = "v3"   # switch between v1, v2, v3


def route_rule_based(intent, user_input):
    if intent == "failure":
        return handle_failure(user_input)
    elif intent == "policy":
        return handle_policy(user_input)
    elif intent == "cost":
        return handle_cost(user_input)
    else:
        return handle_fallback(user_input)


def run_agent():
    print("AUTO-S Agent (Phase 3 - LLM Enabled)\nType 'exit' to quit\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            print("Exiting...")
            break

        intent = classify_intent(user_input)

        if USE_LLM:
            parsed, raw = route_llm_with_rag(intent, user_input)

            # fallback if parsing fails
            if parsed.get("status") == "error":
                response = route_rule_based(intent, user_input)
                print(f"Agent (fallback): {response}\n")
                log_interaction(user_input, response, intent, mode="fallback")
            else:
                print(f"Agent (LLM Parsed): {parsed}\n")
                log_interaction(user_input, parsed, intent, mode="llm")

        else:
            response = route_rule_based(intent, user_input)
            print(f"Agent: {response}\n")
            log_interaction(user_input, response, intent, mode="rule")

# Connect Retrieval to LLM (RAG)
def route_llm_with_rag(intent, user_input):

    retrieved_docs = search(user_input)

    if not retrieved_docs:
        return {
            "status": "escalation",
            "intent": intent,
            "reason": "No relevant knowledge found"
        }

    context = "\n".join(retrieved_docs)

    template = load_prompt(PROMPT_VERSION)

    prompt = template.format(
        query=user_input,
        intent=intent,
        context=context
    )

    return call_llm(prompt)

if __name__ == "__main__":
    run_agent()