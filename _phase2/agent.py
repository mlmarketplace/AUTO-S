import logger

from router import classify_intent
from responders.failure import handle_failure
from responders.policy import handle_policy
from responders.cost import handle_cost
from responders.fallback import handle_fallback
from logger import log_interaction

def run_agent():
    print("AUTO-S Baseline Agent (Type 'exit' to quit)\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            print("Exiting...")
            break

        intent = classify_intent(user_input)

        if intent == "failure":
            response = handle_failure(user_input)
        elif intent == "policy":
            response = handle_policy(user_input)
        elif intent == "cost":
            response = handle_cost(user_input)
        else:
            response = handle_fallback(user_input)

        print(f"Agent: {response}\n")
        log_interaction(user_input, response, intent)


if __name__ == "__main__":
    run_agent()