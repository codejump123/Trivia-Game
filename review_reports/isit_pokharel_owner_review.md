# Review Reports

## Author Template
Role: Author (Code & Unit Test Owner)

### Review Metadata
- Project / Module Name: Trivia Game (Client–Server)
- Author Name: Isit Pokharel
- Review Date: 2026-02-07
- Code Repository / Branch: /Users/isit/Trivia-Game — master

### Unit Description
Provide a concise description of the code under review.

- Purpose of the unit/module:
  Implement a distributed trivia game with authentication, category-based questions,
  wagering, scoring, and persistent user stats. It's meant to be small but complete.
- Primary responsibilities:
  - Server: authenticate users, validate wagers, select questions, score answers,
    persist stats, handle concurrency.
  - Client: CLI flow for login/register, gameplay, and stats display.
  - Protocol: validate/encode/decode JSON message format.
- Key inputs and outputs:
  - Inputs: JSON requests (register, login, get_categories, request_question,
    submit_answer, get_stats, etc.).
  - Outputs: JSON responses with status, payload (question/stats/result), or error
    codes/messages.

### Test Strategy Summary
Explain how the unit is tested.

- Types of tests included:
  Unit tests (core logic, protocol, question selection), system tests
  (client–server flow), edge-case/negative tests (invalid protocol/requests).
- Coverage focus:
  Core logic (wager validation, scoring, stats updates), boundary conditions,
  failure paths in protocol handling.
- Tools/frameworks used:
  Python unittest (python -m unittest discover -s tests).

### Known Limitations or Risks
Be explicit and honest.

- Known limitations:
  - Client stats view does not explicitly show accuracy/win-loss ratio (only points,
    games, correct/incorrect).
  - CLI-only interface (no GUI).
- Technical debt or shortcuts:
  - JSON file storage instead of a database.
  - Simple "recent questions" no-repeat strategy (no adaptive difficulty).
- Assumptions made:
  - Single-machine/local usage.
  - Trusted network and no encrypted transport (no TLS).
- Areas reviewers should pay special attention to:
  - Protocol validation and error handling.
  - Wager validation/scoring edge cases.
  - Data consistency under concurrent access.

### Review Expectations
- Requested focus areas:
  Logic correctness, protocol robustness, test coverage depth, edge cases,
  concurrency behavior.
- Out-of-scope items (if any):
  GUI client, deployment scripts, performance optimization beyond baseline,
  production-grade security.
