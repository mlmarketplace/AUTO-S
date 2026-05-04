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

---

## How to Run

```bash
pip install -r requirements.txt
python agent.py