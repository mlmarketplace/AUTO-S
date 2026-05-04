```
+------------------------------------------------------------+
|                    Business Teams (Users)                   |
|   (Trigger Runs, Raise Issues, Ask Questions)               |
+--------------------------+---------------------------------+
                           |
                           v
+------------------------------------------------------------------+
|                AUTO-S Interaction Layer                          |
|        (Chat Interface / API / CLI / Integrated Chat Bot Tool)   |
+--------------------------+---------------------------------------+
                           |
                           v
+------------------------------------------------------------+
|                Orchestrator Agent (Brain)                   |
|  - Classifies request (failure / policy / cost / support)   |
|  - Routes to appropriate agents                            |
|  - Aggregates responses                                    |
+--------------------------+---------------------------------+
        |            |             |             |
        v            v             v             v

+----------------+  +----------------+  +----------------+  +----------------+
| Failure Agent  |  | Policy Agent   |  | Cost Agent     |  | Support Agent  |
| - Root cause   |  | - Compliance   |  | - Optimization |  | - Q&A / Docs   |
| - Fix suggest  |  | - Violations   |  | - Savings      |  | - Guidance     |
+----------------+  +----------------+  +----------------+  +----------------+
        \                 |                        |             /
         \                |                        |            /
          ------------------------------------------------------
                                 |
                                 v

+------------------------------------------------------------+
|               Safety & Governance Agent                     |
|  - Validates all actions                                   |
|  - Enforces policies                                       |
|  - Handles refusals / escalation                           |
|  - Redacts sensitive data                                  |
+--------------------------+---------------------------------+
                           |
                           v

+------------------------------------------------------------+
|                  MCP Tool Layer (Gateway)                   |
|  - Structured API access                                   |
|  - No direct agent → API calls                             |
|  - Enforces permissions and schemas                        |
+--------------------------+---------------------------------+
                           |
                           v

+------------------------------------------------------------+
|             State Intelligence Service                     |
|  - Normalized Terraform state                              |
|  - Resource relationships (dependency graph)               |
|  - Historical snapshots                                   |
|  - Drift detection                                        |
+--------------------------+---------------------------------+
                           |
                           v

+------------------------------------------------------------+
|            Terraform Enterprise + Cloud APIs                |
|  - Runs, Plans, State                                      |
|  - Policies (Sentinel / OPA)                               |
|  - Cost & usage data                                       |
+------------------------------------------------------------+

```