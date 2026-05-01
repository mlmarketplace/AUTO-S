## Document the exact problem to be solved


### Inputs
1. Terraform run data, plans, and state (sanitized) from Terraform Enterprise
2. Policy definitions and evaluation results from HashiCorp Sentinel / OPA
3. Resource metadata, dependencies, and historical state snapshots
4. Cloud cost and usage data
5. User queries, support tickets, and incident events
6. Structured responses from MCP tools (runs, state, policies, cost)

### Outputs
1. Root cause analysis + recommended actions
2. Risk level and confidence score
3. Explainable reasoning with evidence
4. Safe execution requests or suggestions
5. Refusals and escalation signals
6. Redacted audit logs and system metrics

### Constraints
* Must refuse unsafe or policy-violating actions
* Must not fabricate data (state, policies, cost)
* Must redact secrets/PII from all logs and storage
* Must provide explainable, auditable decisions
* Must enforce role-based access and escalation rules
* No blind LLM decisions—tool-validated only

### Assumptions
* Enterprise uses Terraform Enterprise and defined policies (e.g., HashiCorp Sentinel)
* APIs provide access to runs, state, and cost data
* Environments are segmented (dev/staging/prod)
* Users review/approve high-risk actions
* LLM outputs are always validated via MCP tools