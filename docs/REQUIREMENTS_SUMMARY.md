## Project Requirements Summary

### System overview
- Implement a client-server trivia game with multiple users, authentication, wagering, and persistent statistics.
- Emphasize clean architecture, protocol design, robustness, security, and extensibility.

### Server requirements
- User management: registration, login/logout, secure password storage (hash + salt), persistent user stats.
- Enforce unique usernames and prevent unauthorized access to user data.
- Manage trivia questions by category with question text, options, and correct answer.
- Select questions by category and avoid repeating recently used questions per user.
- Accept and validate wagers, score answers, update stats, and return round results.
- Expose a defined protocol and safely handle malformed client messages.
- Support multiple concurrent clients.

### Client requirements
- Authentication interface with clear feedback and session handling.
- Gameplay flow: category selection, wager input, question display, answer submission, result display.
- Stats view: current points, total questions answered, accuracy or win/loss ratio.
- Interface can be CLI or GUI.

### Testing requirements
- Unit tests for core game logic.
- System tests for client–server communication.

### Deliverables
- Source code for server and client.
- User guide with run instructions and usage.
- Code and unit test review artifacts (review log + report with metrics).
- System test report with strategy and results.

### Review process requirements
- Structured roles: Author, Review Lead, Reviewer, Scribe.
- Severity levels: Blocker, Major, Minor, Nit.
- Mandatory review checklists for code and unit tests.
- Metrics: issues by severity/category, coverage, effort/efficiency, effectiveness.
