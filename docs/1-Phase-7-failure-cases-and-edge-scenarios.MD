# Failure Cases & Edge Scenarios

This system follows a **safety-first, deterministic approach**.  
In uncertain or high-risk situations, it must **refuse or escalate** rather than take action.

---

## 1. Data & State Issues

- **Missing or Corrupted State**
  - State unavailable or invalid  
  - **Action:** Escalate (no assumptions)

- **Drift / Stale State**
  - Infrastructure differs from recorded state  
  - **Action:** Detect and warn before any recommendation

- **Conflicting State Versions**
  - Concurrent updates / race conditions  
  - **Action:** Block actions and escalate

---

## 2. MCP / Tool Failures

- **API Timeout / Failure**
  - Unable to fetch run, state, or policy data  
  - **Action:** Return error, no fallback guessing

- **Partial Tool Responses**
  - Missing fields (e.g., cost, dependencies)  
  - **Action:** Lower confidence, degrade output, possibly escalate

---

## 3. LLM / Reasoning Risks

- **Low Confidence / Ambiguity**
  - Multiple possible root causes  
  - **Action:** Escalate, do not assume

- **Hallucination Risk**
  - No tool-backed evidence  
  - **Action:** Block response

---

## 4. Safety-Critical Scenarios

- **Destructive Actions**
  - Delete resources, force apply  
  - **Action:** Refuse or require explicit approval

- **Active Run Conflicts**
  - Action during active Terraform run  
  - **Action:** Block and explain risk

- **Production Environment Changes**
  - Actions in production workspace  
  - **Action:** Require escalation or approval

---

## 5. Policy & Compliance

- **Ambiguous Policy Results**
  - Partial or unclear evaluation  
  - **Action:** Escalate

- **Missing Policies**
  - No rule defined  
  - **Action:** Do not fabricate, proceed cautiously or escalate

---

## 6. Cost Optimization Edge Cases

- **False Optimization Signals**
  - Low usage but critical resource  
  - **Action:** Flag uncertainty, avoid aggressive changes

- **Incomplete Cost Data**
  - Billing lag or missing inputs  
  - **Action:** Lower confidence, avoid decisions

---

## 7. Dependency & Impact Risks

- **Hidden Dependencies**
  - External/manual dependencies not captured  
  - **Action:** Warn about incomplete analysis

- **High Blast Radius Changes**
  - Core resource affecting multiple services  
  - **Action:** Mark high risk and enforce escalation

---

## 8. Security & Access Control

- **Sensitive Data Exposure**
  - Secrets present in state or logs  
  - **Action:** Mandatory redaction

- **Unauthorized Access**
  - Access to restricted workspace  
  - **Action:** Deny and log violation

---

## 9. User Interaction Edge Cases

- **Vague Queries**
  - "Fix this" without context  
  - **Action:** Request clarification

- **Unsafe User Intent**
  - Bypass policies or risky shortcuts  
  - **Action:** Refuse with explanation

---

## 10. System-Level Failures

- **Agent Conflicts**
  - Conflicting outputs from multiple agents  
  - **Action:** Resolve via orchestrator or escalate

- **Observability Gaps**
  - Missing logs or traces  
  - **Action:** Flag system error, avoid silent failure

---

## Guiding Principle

> When in doubt: **do not act. Escalate.**