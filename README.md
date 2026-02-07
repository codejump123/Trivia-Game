Executive Session, CISC 594  
In class assignment

Team:
- Isit Pokharel
- Durga Sai Sandeep Rayapureddy
- Thien Tan Nguyen
- Dhruv Sharma

# Trivia Game (Client-Server)

This is a simple client-server trivia game for class. The server manages users, questions, and scoring. The client lets you register/login and play rounds by category with a wager. It's small on purpose so the flow is easy to follow.

## How to run

From the project root:

Start the server:
```
python -m server.server --host 127.0.0.1 --port 5000 --data-dir data
```

Start the client in another terminal (run this seperately):
```
python -m client.client --host 127.0.0.1 --port 5000
```

## Notes
- Questions live in `data/questions.json`.
- User data is stored in `data/users.json`.
- If you run it a lot, the `users.json` file will keep growing (that's expected).

## Folder structure
- `client/`: client application (CLI)
- `server/`: server application (threaded TCP)
- `common/`: shared protocol utilities
- `data/`: persistent JSON data (`users.json`, `questions.json`)
- `tests/`: unit and system tests
- `docs/`: documentation and reports
- `review_reports/`: author review templates and notes

## Deliverables
- Source code for client and server (`client/`, `server/`)
- User guide (`docs/USER_GUIDE.md`)
- Code and unit test review artifacts:
  - Review log (`docs/REVIEW_LOG.md`)
  - Review report (`docs/REVIEW_REPORT.md`)
- Author review template (`review_reports/isit_pokharel_owner_review.md`)
- System test report (`docs/SYSTEM_TEST_REPORT.md`)
