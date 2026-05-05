## Evaluation Report

### Methodology

A test harness was used to evaluate:

* Accuracy
* Latency
* Consistency
* Tool reliability

---

### Results

| Metric            | Value     |
| ----------------- | --------- |
| Accuracy          | ~0.85–1.0 |
| Avg Latency       | ~1–2s     |
| Consistency       | ~0.9+     |
| Tool Success Rate | >90%      |

---

### Failure Analysis

#### Case: Follow-up Query Failure

Before:
User: Can I retry now?
→ fallback

Root Cause:

* Intent classified as unknown
* No memory usage

Fix:

* Added memory-aware logic

After:
→ Context-aware response

---

### Observations

* Tool-based flows are highly reliable
* RAG improves explanation quality
* Feedback loop improves behavior

---

### Limitations

* Keyword-based safety detection
* Limited generalization in evaluation
* No bias or fairness testing
