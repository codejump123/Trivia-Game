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
- Meeting Duration: 45 minutes

## Issue Tracking Log
All issues must be logged.

ID | Severity | Category | Reviewer ID | File / Location | Description | Resolution Status | Recommended Fix
--- | --- | --- | --- | --- | --- | --- | ---
1 | Blocker | Functional | Tan | `server/server.py` → `_submit_answer()` | No validation for `answer_index` bounds; malicious/buggy client can send out-of-range values and they are treated as incorrect silently. | Open | Validate `answer_index` is int and within bounds; otherwise return `error_response("Invalid answer_index", "bad_request")`.
2 | Blocker | Functional | Tan | `server/server.py` → `_submit_answer()` | Possible crash if user stats missing (`get_user_stats()` returns `None`, then uses `stats["points"]`). | Open | Guard: `if not stats: return error_response("User not found", "auth_failed")`.
3 | Major | Functional | Tan | `server/game_logic.py` → `update_stats()` | Assumes stats keys always exist and are ints; corrupted payload raises `KeyError`/`TypeError`. | Open | Normalize schema or use safe increments with defaults.
4 | Major | Robustness | Tan | `server/data_store.py` → `_load_json()` | No handling for JSON corruption; server crashes at startup. | Open | Catch `json.JSONDecodeError` and fail fast with clear message or return default and log error.
5 | Major | Functional | Tan | `server/question_bank.py` → `_load_questions()` / `__init__` | No schema validation for questions; missing keys/types cause runtime crashes. | Open | Validate each question on load; list invalid entries.
6 | Major | Functional | Tan | `server/question_bank.py` → `__init__` (_by_id) | Duplicate question IDs silently overwrite in `_by_id`. | Open | Detect duplicates; raise error or skip with warning.
7 | Major | Protocol/Logic | Tan | `common/protocol.py` → `validate_request()` | Only checks presence of fields, not types (e.g., `wager="10"` passes). | Open | Add per-message field type checks (wager int, answer_index int, category str).
8 | Major | Functional | Tan | `server/server.py` → `_request_question()` | Records question as “seen” before round completes; disconnects reduce pool unfairly. | Open | Record “seen” after successful answer or after confirmed send.
9 | Major | Edge Case | Tan | `server/server.py` → session pending logic | Pending question can get stuck if client never answers. | Open | Add timeout or allow abandon/replace pending.
10 | Minor | Edge Case | Tan | `server/game_logic.py` → `validate_wager()` | Wager must be int; JSON `10.0` fails and may confuse clients. | Open | Allow whole-number floats or document strict int requirement.
11 | Minor | Correctness | Tan | `server/data_store.py` → `update_user_stats()` | No validation on stats update; negatives or nonsensical counters possible. | Open | Validate schema/ranges before save.
12 | Minor | Edge Case | Tan | `client/client.py` → `send()` | Empty response on disconnect causes `decode_message("")` to crash. | Open | Catch `ProtocolError` or handle empty response gracefully.
13 | Major | Maintainability | Sai | `client/` | CLI & protocol parsing lacks abstraction. | Open | — 
14 | Minor | Design | Sai | `common/` | Utilities may get overloaded without separation. | Open | —
15 | Minor | Design | Sai | `data/` | JSON format not documented for extensibility. | Open | —
16 | Minor | Test | Sai | `tests/` | Test coverage strategy not explained. | Open | —
17 | Minor | Process | Sai | `docs/` | Module-level design rationale could improve. | Open | —
18 | Minor | Maintainability | Sai | Configuration | Default server host/port fixed; no config file. | Open | —
19 | Major | Design | Sai | `server/` | Logic & networking in one layer; tight coupling. | Open | —
20 | Major | Design | Sai | Concurrency | Concurrent client handling not modularized. | Open | —
21 | Minor | Design | Sai | Error Handling | Malformed client requests not documented. | Open | —
22 | Minor | Maintainability | Sai | Extensibility | Adding new categories requires multi-module changes. | Open | —
23 | Minor | Test | Dhruv | `tests/**` | Provide descriptions/instructions on how to run the test. | Open | Add run instructions or update docs.
24 | Major | Test | Dhruv | `tests/test_question_bank.py` → `test_select_question_fallback` | Non-determinism due to random choice between q1 and q2. | Open | Control RNG or use a fixed seed.
25 | Major | Maintainability | Dhruv | `data/questions.json` | Only 3x3 questions available; game will be short. | Open | Add more questions and categories.
26 | Minor | Test, Performance | Dhruv | `tests/test_system.py` → `test_end_to_end_flow` | Teardown code lacks assertions (may be fine, but unclear). | Open | Add assertions or document teardown intent.
27 | Nit | Test, Design | Dhruv | `tests/test_system.py` → `test_end_to_end_flow` | No setup/teardown methods; could use `setUp()`/`tearDown()`. | Open | Add `setUp()`/`tearDown()` for clarity.
28 | Minor | Test, Design | Dhruv | `tests/test_system.py` → `test_end_to_end_flow` | Magic number `0` in `start_server("127.0.0.1", 0, temp_dir)` (auto-assign port, undocumented). | Open | Document port 0 behavior or use a named constant.
29 | Blocker | Test, Maintainability | Dhruv | `tests/**` | No docstrings/comments explaining test cases and “why”. | Open | Add docstrings/comments for intent.
30 | Nit | Test | Dhruv | `tests/test_system.py` → `test_end_to_end_flow` | Tests 5 operations in one method (violates single responsibility). | Open | Split into smaller tests with focused assertions.
31 | Blocker | Test | Dhruv | `tests/test_system.py` → `test_end_to_end_flow` | Integration test masquerading as unit test; no mocks/stubs; race condition with `time.sleep(0.1)`; flaky risk. | Open | Split into unit vs integration tests; mock sockets, file I/O, and server.
32 | Blocker | Test | Dhruv | `server/game_logic.py` | `apply_answer()` coverage issue; test does not catch bug in `test_game_logic.py` line 26; missing `update_stats` test body. | Open | Add missing test cases and fix the coverage gap.
33 | Blocker | Test | Dhruv | `server/data_store.py` | Missing unit tests for public methods (register/auth/stats/recent questions). | Open | Add unit tests for all public methods.
34 | Blocker | Test | Dhruv | `server/question_bank.py` | Missing unit tests (categories, get_question, select_question edge cases). | Open | Add unit tests for question bank functions.

## Metrics Collection

### Defect & Issue Metrics
- Total issues found: 34
- Blocker: 7
- Major: 13
- Minor: 12
- Nit: 2

By Category:
- Functional defects: 8
- Design issues: 7
- Test deficiencies: 11
- Maintainability/readability: 7
- Process/documentation: 1

### Derived Metrics
- Defects per 1,000 LOC: 28.30  
  Total LOC (source code only, excluding tests): 530  
  Code defects (Functional + Design): 15 issues  
  Calculation: (15 / 530) × 1,000 = 28.30  
  Alternative metric (if counting all issues): 64.15 defects per 1,000 LOC
- % test-related issues: 32.4%  
  Test deficiencies: 11 out of 34 total issues  
  Calculation: (11 / 34) × 100 = 32.4%
- % high-severity issues: 58.8%  
  High-severity (Blocker + Major): 20 out of 34 total issues  
  Blocker: 7, Major: 13  
  Calculation: (20 / 34) × 100 = 58.8%
