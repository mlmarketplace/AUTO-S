from agent.orchestrator import run_agent

if __name__ == "__main__":
    print("=== Agentic IaC Debugger ===\n")

    query = input("Ask your question: ")

    response = run_agent(query)

    print("\n--- Agent Response ---\n")
    print(response)