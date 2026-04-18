mkdir agentic-iac-platform && cd agentic-iac-platform

mkdir -p docs agent/prompts tools workflows safety evaluation/test_cases data/logs data/terraform_states data/sample_configs infra/modules api cli tests scripts

touch README.md LICENSE .env.example requirements.txt docker-compose.yml

touch docs/{architecture.md,design-decisions.md,evaluation.md,failure-analysis.md,demo-scenarios.md}

touch agent/{__init__.py,orchestrator.py,planner.py,executor.py,memory.py}
touch agent/prompts/{system_prompt.txt,security_prompt.txt,debugging_prompt.txt,planning_prompt.txt}

touch tools/{__init__.py,terraform_tool.py,github_tool.py,cloud_tool.py,policy_tool.py,log_parser.py}

touch workflows/{incident_debugging.py,security_validation.py,drift_detection.py}

touch safety/{guardrails.py,approval.py,policy_checks.py}

touch evaluation/{metrics.py,benchmark_tests.py}
touch evaluation/test_cases/{failure_case_1.json,failure_case_2.json,security_case_1.json}

touch infra/{main.tf,variables.tf,outputs.tf}

touch api/{main.py,routes.py,schemas.py}
touch cli/main.py

touch tests/{test_agent.py,test_tools.py,test_workflows.py}

touch scripts/{run_agent.py,simulate_failure.py,setup_env.sh}