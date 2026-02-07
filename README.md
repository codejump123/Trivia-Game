# Trivia Game (Client–Server)

This is a simple client–server trivia game for class. The server manages users, questions, and scoring. The client lets you register/login and play rounds by category with a wager.

## How to run

From the project root:

Start the server:
```
python -m server.server --host 127.0.0.1 --port 5000 --data-dir data
```

Start the client in another terminal:
```
python -m client.client --host 127.0.0.1 --port 5000
```

## Notes
- Questions live in `data/questions.json`.
- User data is stored in `data/users.json`.
