## Example user questions

1. [ ] No free-text-only responses
2. [ ] No missing fields
3. [ ] No guessing when data is absent, return "" appropriate text message

**Global response schema** 
```json lines
{
  "status": "success | refusal | escalation | error",
  "request_id": "string",
  "timestamp": "ISO-8601",
  "intent": "string",
  "data": {},
  "risk_level": "low | medium | high",
  "confidence": 0.0,
  "explanation": "string",
  "evidence": [],
  "recommended_actions": [],
  "safety": {
    "requires_approval": true,
    "policy_violations": [],
    "sensitive": false
  }
}
```

### Ques 1: “Why did my last Terraform run fail in prod, and what’s the safest way to fix it?”

#### Sample JSON Response - Expected
```json
{
  "status": "success",
  "request_id": "req-123",
  "timestamp": "2026-04-29T10:15:00Z",
  "intent": "failure_diagnosis",
  "data": {
    "workspace_id": "ws-prod-1",
    "run_id": "run-456",
    "failure_type": "state_lock",
    "root_cause": "State lock held for 2h by inactive run"
  },
  "risk_level": "low",
  "confidence": 0.92,
  "explanation": "Run failed due to stale state lock exceeding timeout threshold with no active processes.",
  "evidence": [
    {"type": "run_log", "id": "log-1"},
    {"type": "state_lock", "age_minutes": 120}
  ],
  "recommended_actions": [
    {
      "action": "unlock_state",
      "parameters": {"workspace_id": "ws-prod-1"},
      "expected_outcome": "Release lock and allow new run",
      "risk": "low"
    }
  ],
  "safety": {
    "requires_approval": false,
    "policy_violations": [],
    "sensitive": false
  }
}
```
### Ques 2: “Can I safely unlock the state for this workspace, or is something still running?”

#### Sample JSON Response - Expected

```json
{
  "status": "success",
  "request_id": "req-124",
  "timestamp": "2026-04-29T10:18:00Z",
  "intent": "action_validation",
  "data": {
    "workspace_id": "ws-prod-1",
    "action": "unlock_state",
    "active_runs": false,
    "lock_status": "stale"
  },
  "risk_level": "low",
  "confidence": 0.95,
  "explanation": "No active runs detected. Lock is stale beyond threshold.",
  "evidence": [
    {"type": "run_status", "active": false},
    {"type": "lock_age_minutes", "value": 130}
  ],
  "recommended_actions": [
    {
      "action": "unlock_state",
      "parameters": {"workspace_id": "ws-prod-1"}
    }
  ],
  "safety": {
    "requires_approval": false,
    "policy_violations": [],
    "sensitive": false
  }
}
```


### Ques 3: “Why did my plan fail policy checks, and how do I make it compliant?”

#### Sample JSON Response - Expected

```json
{
  "status": "success",
  "request_id": "req-125",
  "timestamp": "2026-04-29T10:20:00Z",
  "intent": "policy_analysis",
  "data": {
    "workspace_id": "ws-dev-2",
    "violations": [
      {
        "policy_name": "restrict_instance_size",
        "resource": "aws_instance.web",
        "issue": "Instance type t3.2xlarge exceeds allowed limit"
      }
    ]
  },
  "risk_level": "medium",
  "confidence": 0.98,
  "explanation": "Instance size exceeds policy threshold defined in Sentinel policy.",
  "evidence": [
    {"type": "policy_result", "policy": "restrict_instance_size"},
    {"type": "plan_diff", "resource": "aws_instance.web"}
  ],
  "recommended_actions": [
    {
      "action": "modify_configuration",
      "parameters": {
        "resource": "aws_instance.web",
        "suggested_instance_type": "t3.medium"
      }
    }
  ],
  "safety": {
    "requires_approval": true,
    "policy_violations": ["restrict_instance_size"],
    "sensitive": false
  }
}
```

### Ques 4: “Which resources in this workspace are over-provisioned, and what can I reduce safely?”

#### Sample JSON Response - Expected

```json
{
  "status": "success",
  "request_id": "req-126",
  "timestamp": "2026-04-29T10:25:00Z",
  "intent": "cost_optimization",
  "data": {
    "workspace_id": "ws-prod-3",
    "total_monthly_cost": 5200,
    "optimization_opportunities": [
      {
        "resource": "aws_instance.api",
        "current_type": "m5.large",
        "suggested_type": "t3.medium",
        "estimated_savings": 1200
      }
    ]
  },
  "risk_level": "medium",
  "confidence": 0.87,
  "explanation": "Resource utilization is below 30%, indicating over-provisioning.",
  "evidence": [
    {"type": "cpu_usage", "value": "25%"},
    {"type": "cost_analysis", "monthly": 1200}
  ],
  "recommended_actions": [
    {
      "action": "modify_configuration",
      "parameters": {
        "resource": "aws_instance.api",
        "new_type": "t3.medium"
      },
      "risk": "medium"
    }
  ],
  "safety": {
    "requires_approval": true,
    "policy_violations": [],
    "sensitive": false
  }
}
```

### Ques 5: “If I change this resource, what else will be affected?”

#### Sample JSON Response - Expected

```json
{
  "status": "success",
  "request_id": "req-127",
  "timestamp": "2026-04-29T10:30:00Z",
  "intent": "dependency_analysis",
  "data": {
    "resource_id": "aws_db_instance.main",
    "affected_resources": [
      {
        "resource": "aws_lambda.processor",
        "dependency_type": "read_connection"
      },
      {
        "resource": "aws_ecs_service.backend",
        "dependency_type": "db_endpoint"
      }
    ]
  },
  "risk_level": "high",
  "confidence": 0.91,
  "explanation": "Multiple services depend on this database endpoint. Changes may disrupt connectivity.",
  "evidence": [
    {"type": "dependency_graph", "edges": 2}
  ],
  "recommended_actions": [
    {
      "action": "proceed_with_caution",
      "parameters": {
        "suggestion": "apply changes in staging first"
      }
    }
  ],
  "safety": {
    "requires_approval": true,
    "policy_violations": [],
    "sensitive": false
  }
}
```

