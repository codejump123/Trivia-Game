# Review Report - Logic & Edge Cases (Thien Tan)

These are the findings from the logic and edge-case review.

## Blockers
1. `server/server.py` → `_submit_answer()` (Functional)  
   The server does not validate `answer_index` bounds. A malicious or buggy client can send a value < 0 or >= `len(options)`. That gets treated as “incorrect” and hides protocol bugs.  
   **Fix:** Validate `answer_index` is an int and `0 <= answer_index < len(question["options"])`. If not, return `error_response("Invalid answer_index", "bad_request")`.

2. `server/server.py` → `_submit_answer()` (Functional)  
   Possible crash if user stats are missing. `get_user_stats()` can return `None` (e.g., corrupted storage), and the code then uses `stats["points"]`.  
   **Fix:** Guard with `if not stats: return error_response("User not found", "auth_failed")`.

## Major Issues
3. `server/game_logic.py` → `update_stats()` (Functional)  
   Assumes all stats keys exist and are ints. If stats are corrupted or partially missing, `+= 1` raises `KeyError`/`TypeError`.  
   **Fix:** Normalize the stats schema before mutation or use safe increments like `stats.get(key, 0)`.

4. `server/data_store.py` → `_load_json()` (Robustness)  
   Does not handle JSON corruption (`JSONDecodeError`). If `users.json` is empty/invalid, the server crashes at startup.  
   **Fix:** Catch `json.JSONDecodeError` and either fail fast with a clear message or return defaults and log the issue.

5. `server/question_bank.py` → `_load_questions()` / `__init__` (Functional)  
   No schema validation for questions. Missing keys or wrong types can cause runtime crashes later.  
   **Fix:** Validate each question on load and raise a clear error listing invalid entries.

6. `server/question_bank.py` → `__init__` (_by_id) (Functional)  
   Duplicate question IDs silently overwrite each other. That can break correctness.  
   **Fix:** Detect duplicates on load and raise an error (or skip with a warning).

7. `common/protocol.py` → `validate_request()` (Protocol/Logic)  
   Only checks presence of fields, not types. Example: `wager="10"` passes validation but fails later.  
   **Fix:** Add per-message field type checks (e.g., `wager` int, `answer_index` int, `category` str).

8. `server/server.py` → `_request_question()` (Functional)  
   The server records a question as “seen” before the round completes. If the client disconnects, the question is still removed from the pool.  
   **Fix:** Record “seen” after a successful answer submission, or track pending and commit on completion.

9. `server/server.py` → session pending logic (Edge Case)  
   Pending questions can get stuck if a client never answers. That blocks gameplay for that connection.  
   **Fix:** Add a timeout or allow a new question to replace pending (explicit “abandon”).

## Minor Issues
10. `server/game_logic.py` → `validate_wager()` (Edge Case)  
   Wager must be int, so JSON `10.0` fails. That’s fine but can confuse clients.  
   **Fix:** Either allow whole-number floats or document the strict int requirement clearly.

11. `server/data_store.py` → `update_user_stats()` (Correctness)  
   No validation on stats updates. A bug could write negative points or nonsensical counters.  
   **Fix:** Validate schema/ranges before saving (points >= 0, counters >= 0, ints).

12. `client/client.py` → `send()` (Edge Case)  
   If the server closes the connection, `reader.readline()` may return empty, and `decode_message("")` raises. The client crashes.  
   **Fix:** Catch `ProtocolError` or handle empty response, show “Disconnected” and exit gracefully.
