## Trivia Game User Guide

### Prerequisites
- Python 3.9+ installed.

### Project layout
- `server/`: trivia server code.
- `client/`: trivia client code.
- `data/`: persistent data (`users.json`, `questions.json`).
- `tests/`: unit and system tests.
- `docs/`: reports and documentation.

### Run the server
From the project root:
```
python -m server.server --host 127.0.0.1 --port 5000 --data-dir data
```

### Run the client
In a seperate terminal from the project root:
```
python -m client.client --host 127.0.0.1 --port 5000
```

### Gameplay flow
- Register a new account or login.
- Choose a trivia category and enter a wager.
- Answer the question and see the result.
- View stats at any time to see points and accuracy.

### Run tests
```
python -m unittest discover -s tests
```
