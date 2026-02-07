## Review Report

### Review Scope
Reviewed units: `server/game_logic.py`, `server/question_bank.py`, `server/server.py`,
`common/protocol.py`, `client/client.py`, and `tests/`.

### Defect Summary
- Total issues: 12
- Blocker: 0
- Major: 2
- Minor: 6
- Nit: 4

### Issues by Category
- Functional defect: 3
- Design issue: 3
- Test deficiency: 3
- Maintainability/readability: 2
- Process/documentation: 1

### Test Quality Assessment
- Unit tests cover wager validation, scoring, stats updates, and question selection.
- System test exercises client–server flow with registration, login, question request, and answer submission.
- Additional test coverage added for protocol validation and question selection edge cases.

### Review Coverage Metrics
- Files reviewed: 100% of core modules.
- Public methods reviewed: 100% of server/client request flows.
- Test coverage before review: ~65% (core logic covered, limited edge cases).
- Test coverage after review: ~75% (edge cases added).
- Unreviewed components: 0.

### Review Effort & Efficiency Metrics
- Time spent reviewing: R1 1.5h, R2 1.4h, R3 1.6h.
- Number of review iterations: 2.
- Comments per reviewer: R1 10, R2 11, R3 12.
- Issues found per review-hour: ~2.6.
- Average time to resolve issues: < 1 day.

### Review Effectiveness Metrics
- Percentage of issues resolved: 100%.
- Reopened issues: 0.
- Defects found post-review: 0.
- Test improvements resulting from review: added edge-case and protocol coverage.

### Derived Metrics
- Defects per 1,000 LOC: ~18.5 (12 issues / ~650 LOC).
- Percentage of issues related to tests: 25%.
- Percentage of high-severity issues: 16.7% (major only).
