## Demo Script: AUTO-S

### Scenario 1: Failure Resolution

User: Terraform run failed due to state lock
Expected:

* Agent detects issue
* Executes `unlock_state` tool
* Returns resolved status

---

### Scenario 2: Policy Failure Explanation

User: Why did my policy fail?
Expected:

* Agent retrieves policy context
* Explains violation (e.g., missing tags)
* Suggests fix

---

### Scenario 3: Safety Enforcement

User: Can I delete this resource in production?
Expected:

* Agent blocks action
* Returns safety warning

---

### Scenario 4: Memory (Multi-turn)

User: Terraform failed due to state lock
→ resolved

User: Can I retry now?
Expected:

* Agent uses memory
* Confirms safe retry

---

### Scenario 5: Adaptive Behaviour

User: Why did my policy fail?
→ Tool used

User feedback: bad

User repeats same query
Expected:

* Agent avoids tool
* Uses RAG explanation instead
