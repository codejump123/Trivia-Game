## Architecture Overview

### Components
- Server: authoritative game state, authentication, question selection, scoring, persistence.
- Client: user-facing CLI that drives authentication, gameplay, and stats display.
- Shared protocol: JSON line messages between client and server.

### Modules
- `server/auth.py`: password hashing and verification.
- `server/data_store.py`: persistent users and stats (JSON).
- `server/question_bank.py`: question loading, category listing, no-repeat selection.
- `server/game_logic.py`: wager validation, scoring, stat updates.
- `server/server.py`: threaded TCP server and request handling.
- `client/client.py`: CLI client and request flow.
- `common/protocol.py`: message encoding/decoding and validation.

### Persistence
- Users stored in `data/users.json` with password hashes, salts, stats, and recent questions.
- Questions stored in `data/questions.json` as a list of records with category and correct answer.

### Protocol (JSON line)
Each request/response is a JSON object delimited by `\\n`.

Requests:
- `register`: `{type, username, password}`
- `login`: `{type, username, password}`
- `logout`: `{type}`
- `get_categories`: `{type}`
- `request_question`: `{type, category, wager}`
- `submit_answer`: `{type, question_id, answer_index}`
- `get_stats`: `{type}`
- `ping`: `{type}`

Responses:
- Success: `{status: "ok", ...payload}`
- Error: `{status: "error", code, message}`

### Concurrency
- Threaded TCP server supports multiple simultaneous clients.
- DataStore uses a lock to ensure consistent user updates.
