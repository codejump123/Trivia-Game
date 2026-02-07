---
title: "Scribe Role"
author: "Dhruv Sharma"
date: "2026-02-07"
output: github_document
---

# Role: Scribe / Quality Engineer

## Review Session Information
- Scribe Name: Dhruv Sharma
- Review Date: 07 Feb 2026
- Participants: Dhruv Sharma, Isit Pokharel, Durga Sai Sandeep Rayapureddy, Thien Tan Nguyen
- Meeting Duration: (not recorded)

## Issue Tracking Log
All issues must be logged.

## Issues

1. **`server/server.py` → `_submit_answer()`**  
   **Severity:** Blocker  
   **Category:** Functional  
   **Finding:** No validation for `answer_index` bounds. A malicious/buggy client can send
   `answer_index < 0` or `>= len(options)`. Treated as incorrect silently, masking protocol bugs.  
   **Recommended Fix:** Validate `answer_index` is int and within bounds; otherwise return
   `error_response("Invalid answer_index", "bad_request")`.

2. **`server/server.py` → `_submit_answer()`**  
   **Severity:** Blocker  
   **Category:** Functional  
   **Finding:** Possible crash if user stats missing. `get_user_stats()` can return `None`,
   then code uses `stats["points"]`.  
   **Recommended Fix:** Guard `if not stats: return error_response("User not found", "auth_failed")`.

3. **`server/game_logic.py` → `update_stats()`**  
   **Severity:** Major  
   **Category:** Functional  
   **Finding:** Assumes stats keys always exist and are ints; corrupted payload causes
   `KeyError`/`TypeError`.  
   **Recommended Fix:** Normalize schema or use safe increments with defaults.

4. **`server/data_store.py` → `_load_json()`**  
   **Severity:** Major  
   **Category:** Robustness  
   **Finding:** No handling for JSON corruption (`JSONDecodeError`); server crashes at startup.  
   **Recommended Fix:** Catch decode errors and fail fast with clear message or return defaults.

5. **`server/question_bank.py` → `_load_questions()` / `__init__`**  
   **Severity:** Major  
   **Category:** Functional  
   **Finding:** No schema validation for questions; missing keys/types cause runtime crashes.  
   **Recommended Fix:** Validate each question on load; report invalid entries.

6. **`server/question_bank.py` → `__init__` (_by_id)**  
   **Severity:** Major  
   **Category:** Functional  
   **Finding:** Duplicate IDs silently overwrite in `_by_id`.  
   **Recommended Fix:** Detect duplicates; raise error or skip with warning.

7. **`common/protocol.py` → `validate_request()`**  
   **Severity:** Major  
   **Category:** Protocol/Logic  
   **Finding:** Only checks field presence, not types (e.g., `wager="10"` passes).  
   **Recommended Fix:** Add per-message type checks for required fields.

8. **`server/server.py` → `_request_question()`**  
   **Severity:** Major  
   **Category:** Functional  
   **Finding:** Records question as “seen” before round completes; disconnects reduce pool unfairly.  
   **Recommended Fix:** Record “seen” after answer submission or after confirmed send.

9. **`server/server.py` → session pending logic**  
   **Severity:** Major  
   **Category:** Edge Case  
   **Finding:** Pending question can get stuck if client never answers.  
   **Recommended Fix:** Add timeout or allow abandon/replace pending.

10. **`server/game_logic.py` → `validate_wager()`**  
    **Severity:** Minor  
    **Category:** Edge Case  
    **Finding:** Wager must be int; JSON `10.0` fails and may confuse clients.  
    **Recommended Fix:** Allow whole-number floats or document strict int requirement.

11. **`server/data_store.py` → `update_user_stats()`**  
    **Severity:** Minor  
    **Category:** Correctness  
    **Finding:** No validation on stats update; negatives or nonsensical counters possible.  
    **Recommended Fix:** Validate schema/ranges before save.

12. **`client/client.py` → `send()`**  
    **Severity:** Minor  
    **Category:** Edge Case  
    **Finding:** Empty response on disconnect causes `decode_message("")` to crash.  
    **Recommended Fix:** Catch `ProtocolError` or handle empty response gracefully.

## Metrics Collection

### Defect & Issue Metrics
- Total issues found:
- Blocker:
- Major:
- Minor:
- Nit:

By Category:
- Functional defects:
- Design issues:
- Test deficiencies:
- Maintainability/readability:
- Process/documentation:

### Derived Metrics
- Defects per 1,000 LOC:
- % test-related issues:
- % high-severity issues:
