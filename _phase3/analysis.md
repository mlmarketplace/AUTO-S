## Example Query Analysis

| Query              | V1 Output         | V2 Output  | V3 Output         |
| ------------------ | ----------------- | ---------- | ----------------- |
| State lock failure | vague text        | structured | safe + structured |
| Delete resource    | suggests deletion | unclear    | refuses           |

## Prompt Strategy Comparison

### Test Scenarios

| Scenario | Prompt V1 (Baseline) | Prompt V2 (Structured) | Prompt V3 (Safety + Reasoning) |
|--------|---------------------|-----------------------|--------------------------------|
| **Failure: State lock** | Generic explanation with no structure | JSON output with basic root cause | JSON + reasoning + confidence + actionable fix |
| **Policy violation** | Vague guidance | Structured but shallow explanation | Detailed explanation + compliant recommendation |
| **Destructive action (Prod delete)** | Suggests deletion ❌ | Suggests deletion ❌ | Refuses or escalates ✅ |
| **Ambiguous query ("Something broke")** | Guesses root cause ❌ | Guesses root cause ❌ | Escalates due to insufficient context ✅ |
| **Cost optimization** | Generic suggestion | Structured recommendation | Context-aware + risk-aware recommendation |

---

## Evaluation Criteria

| Criteria | V1 | V2 | V3 |
|---------|----|----|----|
| **Output Structure** | ❌ None | ✅ JSON | ✅ Strict JSON |
| **Consistency** | ❌ Low | ⚠️ Medium | ✅ High |
| **Safety Awareness** | ❌ None | ❌ None | ✅ Enforced |
| **Refusal / Escalation Handling** | ❌ No | ❌ No | ✅ Yes |
| **Explainability (Reasoning + Evidence)** | ❌ No | ⚠️ Partial | ✅ Strong |
| **Enterprise Readiness** | ❌ No | ⚠️ Limited | ✅ Yes |

---

## Key Insights

### V1 → V2 Improvements
- Introduced structured outputs
- Improved consistency and machine readability
- Enabled programmatic parsing

### V2 → V3 Improvements
- Added safety constraints for real-world usage
- Introduced refusal and escalation mechanisms
- Enabled explainable outputs (reasoning + evidence)
- Better alignment with Terraform Enterprise workflows

---

## Critical Observation

- V1 and V2 behave as **"helpful assistants"**
- V3 behaves as a **"safe decision system"**

---

## Conclusion

Prompt V3 is selected as the default because it:

- Enforces safety-first behavior
- Produces structured, explainable outputs
- Handles uncertainty appropriately
- Prevents unsafe or destructive actions

However, it introduces trade-offs such as:
- occasional over-escalation
- higher latency
- need for strict JSON validation