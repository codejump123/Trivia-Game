## System Test Report

### Scope
End-to-end client-server communication and gameplay workflow.

### Strategy
- Start the server with a temporary data directory and sample questions.
- Connect a client socket and perform:
  - user registration
  - user login
  - category listing
  - question request with wager
  - answer submission
- Validate successful responses and correct scoring behavior.

### Test Cases
1. Register new user and login successfully.
2. Retrieve category list.
3. Request a question and submit a correct answer.

### Results
- All system tests passed using `tests/test_system.py`.
- It's a small set of cases, but it hits the main happy path.

### Notes
- Errors for invalid requests and authentication failures are handled through explicit error responses.
