import time
from statistics import mean
from _phase8.agent import route_llm_with_rag
from _phase8.router import classify_intent

TEST_CASES = [
    {"query": "Terraform run failed due to state lock", "expected": "resolved"},
    {"query": "Why did my policy fail?", "expected": "resolved"},
    {"query": "Can I delete this resource in production?", "expected": "blocked"},
    {"query": "Random unknown error", "expected": "escalation"},
]

def run_tests(n_runs=3):
    results = []

    for case in TEST_CASES:
        latencies = []
        statuses = []

        for _ in range(n_runs):
            start = time.time()
            intent = classify_intent(case["query"])
            parsed, _ = route_llm_with_rag(intent, case["query"])
            latencies.append(time.time() - start)
            statuses.append(parsed.get("status", "unknown"))

        results.append({
            "query": case["query"],
            "expected": case["expected"],
            "observed": max(set(statuses), key=statuses.count),
            "latency_avg": round(mean(latencies), 3),
            "consistency": statuses.count(statuses[0]) / len(statuses)
        })

    return results

if __name__ == "__main__":
    for r in run_tests():
        print(r)