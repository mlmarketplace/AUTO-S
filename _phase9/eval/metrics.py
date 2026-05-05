def compute_metrics(results):
    total = len(results)
    correct = sum(1 for r in results if r["expected"] == r["observed"])
    avg_latency = sum(r["latency_avg"] for r in results) / total
    consistency = sum(r["consistency"] for r in results) / total

    return {
        "accuracy": round(correct / total, 2),
        "avg_latency": round(avg_latency, 2),
        "consistency": round(consistency, 2)
    }