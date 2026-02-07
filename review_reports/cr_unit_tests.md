---
title: "CR Unit Tests"
author: "Dhruv Sharma"
date: "2026-02-07"
output: github_document
---

# Role: Reviewer

- Reviewer Name: Dhruv Sharma  
- Assigned Focus Area: Unit Tests  
- Time Spent Reviewing (hours): 1–1.5 hrs

# Findings Log

Log at least 10 comments, meeting minimum expectations.

## Issues

1. **`tests/**`**  
   Running `python tests/test_game_logic.py` fails with:  
   `ModuleNotFoundError: No module named 'server'`  
   **Finding:** Provide descriptions/instructions on how to run the test.  
   **Severity:** Minor  
   **Category:** Test

2. **`tests/test_question_bank.py` → `test_select_question_fallback`**  
   **Finding:** Non-determinism since there is a random choice between 2 questions (q1, q2).  
   **Severity:** Major  
   **Category:** Test

3. **`data/questions.json`**  
   **Finding:** Only 3x3 questions available; game will be short.  
   **Severity:** Major  
   **Category:** Maintainability

4. **`tests/test_system.py` → `test_end_to_end_flow`**  
   **Finding:** Teardown code lacks assertions. Logical test assertions are present.  
   **Severity:** Minor  
   **Category:** Test, Performance

5. **`tests/test_system.py` → `test_end_to_end_flow`**  
   **Finding:** No setup/teardown methods; could use `setUp()` and `tearDown()` for clarity.  
   **Severity:** Nit  
   **Category:** Test, Design

6. **`tests/test_system.py` → `test_end_to_end_flow`**  
   **Finding:** Magic number `0` in `start_server("127.0.0.1", 0, temp_dir)` (port 0 means auto-assign, but undocumented).  
   **Severity:** Minor  
   **Category:** Test, Design

7. **`tests/**`**  
   **Finding:** No docstrings/comments explaining test cases and “why”.  
   **Severity:** Blocker  
   **Category:** Test, Maintainability

8. **`tests/test_system.py` → `test_end_to_end_flow`**  
   **Finding:** Tests 5 operations in one method (violates single responsibility).  
   **Fix:** Split into 5 helper tests with individual assertions.  
   **Severity:** Nit  
   **Category:** Test

9. **`tests/test_system.py` → `test_end_to_end_flow`**  
   **Finding:** Integration test masquerading as a unit test.  
   - Tests entire system  
   - No mock server (`unittest.mock.Mock` / `patch` missing)  
   - No stubbed sockets (`MagicMock`)  
   - No mocked file I/O (`patch("builtins.open")`)  
   - Race condition (`time.sleep(0.1)` is fragile)  
   - Flaky test risk  
   **Severity:** Blocker  
   **Category:** Test

10. **`server/game_logic.py`**  
    **Finding:** Issues with `apply_answer()` coverage. Test doesn't catch a bug in `test_game_logic.py` line 26.  
    Missing test cases; `update_stats` test body is missing.  
    **Verdict:** Partially tested  
    **Severity:** Blocker  
    **Category:** Test

11. **`server/data_store.py`**  
    **Finding:** Missing unit tests for public methods.  
    Suggested tests:  
    - `register_user()` valid + duplicate + empty password  
    - `authenticate()` correct + wrong + nonexistent user  
    - `get_user_stats()` default stats  
    - `update_user_stats()` persists changes  
    - `record_question_seen()` tracks questions  
    - `get_recent_questions()` returns recent only  
    **Severity:** Blocker  
    **Category:** Test

12. **`server/question_bank.py`**  
    **Finding:** Missing unit tests.  
    Suggested tests:  
    - `get_categories()` unique + sorted  
    - `get_question(valid_id)` + `get_question(invalid_id)`  
    - `select_question()` invalid category  
    - `select_question()` all recent  
    - `select_question()` no questions in category  
    **Severity:** Blocker  
    **Category:** Test

# Summary of Key Issues

- **Top 3 high-severity issues:**  
  - Missing unit tests for various public methods  
  - Integration test disguised as unit test, should be split into smaller assertable tests  
  - No docstrings/comments explaining the testing, and hardcoded values  

- **Most concerning design or test gap:**  
  - Did not catch a bug in `test_game_logic.py` line 26  
  - Missing unit test cases for various public methods

# Reviewer Recommendation

- [ ] Approve  
- [ ] Approve with changes  
- [x] Block

**Reasoning:** More than 3 issues present with “Blocker” severity.
