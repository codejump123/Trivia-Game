## Review Log
Raw list of findings from the review sessions.

### Review Scope
Units reviewed: `server/game_logic.py`, `server/question_bank.py`, `server/server.py`, `common/protocol.py`, `client/client.py`, `tests/`.

### Issue Log
| Issue ID | File/Location | Severity | Category | Reviewer | Resolution |
| --- | --- | --- | --- | --- | --- |
| R-001 | `server/game_logic.py` wager validation | Major | Functional defect | R1 | Resolved |
| R-002 | `server/game_logic.py` stats update | Minor | Maintainability/readability | R2 | Resolved |
| R-003 | `server/question_bank.py` no-repeat logic | Minor | Design issue | R1 | Resolved |
| R-004 | `server/question_bank.py` missing category handling | Minor | Functional defect | R2 | Resolved |
| R-005 | `common/protocol.py` invalid JSON handling | Major | Design issue | R3 | Resolved |
| R-006 | `server/server.py` pending question state | Minor | Design issue | R3 | Resolved |
| R-007 | `server/server.py` error response codes | Nit | Maintainability/readability | R1 | Resolved |
| R-008 | `client/client.py` input validation for wager | Minor | Functional defect | R2 | Resolved |
| R-009 | `tests/test_system.py` missing negative path | Minor | Test deficiency | R3 | Resolved |
| R-010 | `tests/test_protocol.py` coverage for unknown type | Nit | Test deficiency | R2 | Resolved |
| R-011 | `tests/test_question_bank.py` edge case coverage | Nit | Test deficiency | R1 | Resolved |
| R-012 | `docs/USER_GUIDE.md` run instructions clarity | Nit | Process/documentation | R2 | Resolved |
