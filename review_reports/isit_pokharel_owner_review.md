# Owner Review - Isit Pokharel

## Review Overview
- Project / Module Name: Trivia Game (Client-Server)
- Author Name: Isit Pokharel
- Role: Author (Code & Unit Test Owner)
- Review Date: 2026-02-07
- Code Repository / Branch: /Users/isit/Trivia-Game — master

## Scope
Reviewed core modules for gameplay flow, protocol handling, and persistence:
`server/`, `client/`, `common/`, and `tests/`.

## Quick Summary
The overall flow works and tests pass, but there are a few usability and robustness
items worth tracking (mostly minor).

## Findings (Owner Review)
1. `client/client.py` → stats view (Minor, Usability)  
   Stats display does not show accuracy or win/loss ratio explicitly (only points,
   games played, correct/incorrect).  
   **Fix:** Add a calculated accuracy line (e.g., correct / total * 100).

2. `server/data_store.py` → persistence (Minor, Robustness)  
   JSON files are the only storage option. It is simple but fragile if files are
   edited manually or corrupted.  
   **Fix:** Add light validation or a safer fallback when JSON is invalid.

3. `server/question_bank.py` → no-repeat logic (Minor, Design)  
   The recent-question strategy is intentionally simple and does not consider
   difficulty or long-term balancing.  
   **Fix:** Keep as-is for scope, or extend later with per-category weighting.

4. `common/protocol.py` → request validation (Minor, Clarity)  
   Validation is minimal and leaves type checks to later stages. This can make
   error messages feel inconsistent.  
   **Fix:** Add optional type checks for common fields (wager, answer_index, category).

## Test Strategy
- Unit tests cover core logic (wager validation, scoring, stats updates).
- System tests exercise a basic end-to-end gameplay path.
- Tools: Python unittest (`python -m unittest discover -s tests`).

## Assumptions / Notes
- CLI-only interface is acceptable for the assignment.
- Local, trusted environment (no TLS).
- JSON persistence is fine for course scope.
