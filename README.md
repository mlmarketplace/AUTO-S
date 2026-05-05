# AUTO-S

## Autonomous Enterprise Terraform Platform Operations & Support System

### Built for Stability, Security, and Scalability

#### Reduces MTTR and support load for Terraform Enterprise platform teams

---

**Author:** Abhishek Junnarkar  

**Powered by a safety-first multi-agent system with MCP tools and a state intelligence layer**

---

AUTO-S is a safety-first, AI-powered system built to support the Terraform Enterprise platform team in diagnosing, reasoning about, and resolving infrastructure issues across the organization.

It continuously analyzes Terraform runs, state, and policies to identify root causes, recommend or safely execute fixes, and enforce compliance. By combining multi-agent decision-making with a controlled MCP tool layer and structured state intelligence, AUTO-S reduces MTTR, minimizes manual support effort, and standardizes resolution workflows—enabling faster, safer outcomes for both the platform team and business teams.

---

## Architecture Overview

![AUTO-S Architecture](_evolution_phase1_docs/auto_s_architecture_diagram.svg)

### Layer Highlights

- **Business Teams → Interaction Layer**  
  Entry point for developers, SREs, FinOps, and security engineers  

- **Orchestrator**  
  Classifies intent across failure, policy, cost, and support  

- **Specialized Agents**  
  - Failure (coral)  
  - Policy (amber)  
  - Cost (green)  
  - Support (blue)  

- **Safety & Governance Layer**  
  Enforces zero unsafe actions  

- **MCP Tool Layer**  
  Prevents direct agent-to-API access  

- **State Intelligence Layer**  
  Handles drift detection, dependency graphs, history  

- **Backend Systems**  
  Terraform runs, policy engines, cost data  

---

## Phase 1: Problem Understanding & Success Definition

### Deliverables

- Personas  
- Problem Statement  
- Inputs / Outputs / Constraints  
- Example User Questions  
- Success Criteria  
- Failure Cases & Edge Scenarios  

---

## Overview

This project builds an **AI-powered agentic platform** to transform enterprise infrastructure operations.

### Key Value

- Interprets failures  
- Enforces compliance  
- Guides decisions  
- Automates repetitive tasks  

👉 Core ROI: **Reliable, explainable decision augmentation**

---

## Domain Understanding & Problem Framing

### Enterprise Context

Designed for the **Terraform Enterprise (TFE) platform team** supporting organization-wide infrastructure usage.

### Current Workflow

1. Business team triggers Terraform run  
2. Failure or unclear output  
3. Support ticket raised  
4. Platform engineer investigates  
5. Fix is suggested/applied  
6. Response returned  

### Problems

1. **Support Bottleneck**  
2. **High MTTR**  
3. **Fragmented Context**  
4. **Inconsistent Decisions**  
5. **Operational Risk**

---

## Problem Statement

The Terraform Enterprise team acts as a **manual decision layer**, lacking:

- unified reasoning across runs, state, policies  
- real-time diagnostics  
- automated safe remediation  

👉 Result:
- high operational load  
- slow resolutions  
- inconsistent outcomes  

---

## Users

### Primary
- Terraform Platform Team (SRE / DevOps)

### Secondary
- Business Teams using Terraform

---

## Solution

### Architecture

A **multi-agent, safety-first system** with:

- MCP tool layer  
- State intelligence  
- LLM reasoning  

### Core Capabilities

| Capability | Description |
|-----------|------------|
| Root Cause Analysis | Explain failures clearly |
| Policy Enforcement | Prevent violations |
| Decision Guidance | Recommend safe actions |
| Automation | Execute repeatable tasks |

---

## Inputs

- Terraform runs, plans, state  
- Policy outputs  
- Cost data  
- User queries  
- MCP tool responses  

---

## Outputs

- Root cause + recommendations  
- Risk + confidence  
- Evidence-backed reasoning  
- Safe actions or escalation  

---

## Constraints

- No unsafe actions  
- No hallucination  
- Full auditability  
- RBAC enforced  

---

## Assumptions

- Terraform Enterprise exists  
- Policies are defined  
- APIs available  
- Human approval for risk  

---

## Example Questions

- Why did my Terraform run fail?  
- Can I safely unlock state?  
- Why did policy fail?  
- Which resources are over-provisioned?  

---

## Success Criteria

### Operational
- 40–60% MTTR reduction  
- ≥50% auto-resolution  

### Safety
- 0 unsafe actions  
- 100% correct refusal  

### Reliability
- ≥99% uptime  

---

## Failure Cases

- Missing state → escalate  
- Drift → warn  
- API failure → no guessing  
- Destructive request → refuse  

---

## Phase 2: Baseline Agent

### Objective
Build a rule-based CLI agent.

### Features
- Intent classification  
- Modular responders  
- Logging  

### Limitations

- No context awareness  
- No real data  
- No safety validation  

---

## Phase 3: LLM Integration

### Prompt Versions

| Version | Description |
|--------|------------|
| V1 | Unstructured |
| V2 | Structured |
| V3 | Safety + Reasoning |

### Key Improvements

- Structured outputs  
- Safety enforcement  
- Explainability  

### Limitations

- JSON parsing issues  
- Over-escalation  
- Prompt sensitivity  

---

## Phase 4: Knowledge Integration & Semantic Retrieval (RAG)

### Overview

Introduces **FAISS-based retrieval** to ground responses in real Terraform knowledge.

### Pipeline

1. Documents → chunked  
2. Chunks → embedded  
3. Stored in FAISS  
4. Query → similarity search  
5. Context → injected into prompt  

---

### Retrieval Evaluation

| Query | Retrieved Context | Relevance | Behaviour |
|------|------------------|----------|----------|
| State lock issue | Causes + fix | High | Accurate |
| Policy failure | Rules + constraints | High | Context-aware |
| Cost optimization | Strategies | Medium | Structured output |
| Delete resource | No context | Low | Escalation |
| Kubernetes error | Weak match | Low | Refusal |

---

### Before vs After

| Scenario | Without RAG | With RAG |
|---------|------------|----------|
| State lock | Generic | Accurate |
| Policy | Vague | Grounded |
| Cost | Generic | Context-aware |
| Unknown | Hallucination | Safe refusal |

---

### Key Observations

- Retrieval improves accuracy  
- Reduces hallucination  
- Enables safe fallback  

---

### Limitations

- Limited to indexed docs  
- No reranking  
- Partial matches possible  

---

### Conclusion

FAISS-based RAG transforms the agent into a:

👉 **Context-aware, safety-first decision system**

## Phase 5: Tool-Using Agent

### Overview

Phase 5 extends AUTO-S from a reasoning system into an **action-capable agent** by enabling controlled tool usage.

The agent can now:
- Decide **when** to use a tool  
- Select the **correct tool** based on user intent  
- Execute tools safely  
- Incorporate tool outputs into reasoning  
- Prevent unsafe or incorrect actions  

This transforms the system from:
> “AI that explains problems” → “AI that can act on problems safely”

---

## Tool Design

Tools are designed to reflect realistic Terraform Enterprise operations.

### Implemented Tools

| Tool | Purpose | Example Use |
|-----|--------|------------|
| `get_run_status` | Fetch Terraform run status | Debug failed run |
| `unlock_state` | Unlock Terraform state | Resolve state lock |

---

## Tool Registry

All tools are centrally defined in a registry for consistency and scalability.

```python
TOOLS = {
    "get_run_status": {
        "description": "Fetch Terraform run status",
        "args": ["run_id"]
    },
    "unlock_state": {
        "description": "Unlock Terraform state",
        "args": ["workspace"]
    }
}
```
---

## Phase 6: Planning, Memory & Context

### Overview

## Phase 6 enhances AUTO-S with **stateful intelligence** by introducing:

- Multi-step planning
- Short-term conversational memory
- Context-aware reasoning across turns

This transforms the agent from a reactive system into a **context-aware decision engine**.

---

## Architecture Update

User → Intent → Memory → Planner → Tool/RAG → Memory Update → Response

---

## Planning Capability

The system decomposes tasks into structured steps:

| Scenario | Plan |
|--------|------|
| State Lock | identify_issue → unlock_state → confirm |
| Policy Failure | identify_issue → fetch_policy → suggest_fix |
| Cost Optimization | analyze → detect_waste → optimize |

This ensures:
- structured reasoning  
- explainable decision flow  

---

## Memory System

### Type: Short-Term Memory

Stores recent interactions:

- user queries  
- agent responses  

---

### Memory Behavior

| Feature | Implementation |
|--------|--------------|
| Retention | Last 5 interactions |
| Reset | `reset` command |
| Usage | Injected into LLM prompt |

---

### Example

**Turn 1**
User: Terraform failed due to state lock  
→ resolved  

**Turn 2**
User: Can I retry now?  
→ Agent uses memory → “Yes, issue was resolved”

---

## Multi-Turn Improvement

| Before | After |
|------|------|
| No context awareness | Remembers past issues |
| Generic answers | Context-aware responses |
| Stateless | Stateful reasoning |

---

## Impact

- Improved user experience  
- Reduced repeated explanations  
- Better decision continuity  
- More human-like interaction  

---

## Limitations

- Only short-term memory  
- No long-term persistence  
- No semantic memory retrieval  

---

## Conclusion

Phase 6 enables AUTO-S to:

- remember context  
- plan actions  
- reason across multiple steps  

This aligns the system with real-world **agentic AI architectures** used in enterprise environments.

## How to Run

```bash
pip install -r requirements.txt
python agent.py