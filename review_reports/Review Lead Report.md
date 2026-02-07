# Review Lead Template

## Role
Review Lead

## Review Overview
- Review Lead Name: Tan Nguyen
- Module / Component Under Review: Trivia-game
- Review Type: Code review

## Scope & Objectives
- Primary goals of this review:
  This review is to validate that Trivia-game can fulfill these requirements:
  The server hosts trivia questions, manages user accounts and game logic, and
  persists data. Clients connect to the server, authenticate users, request
  questions, submit answers, and display game state.

- Critical risk areas:
  - Concurrency & multi-client handling (server)
  - Security of authentication & user data
  - Communication protocol robustness
  - Game logic integrity (authoritative server)
  - Persistence & data consistency
  - Client-server state synchronization
  - Client UI logic
  - Test coverage & quality

- Acceptance criteria for merge:
  - Server able to host trivia questions
  - Server can manage accounts, and authenticate users
  - Server can provide data and statistics for users
  - Client can connect to server
  - Client can request questions from server
  - Client can submit answer to server
  - Client can display current score, statistic, and answer from server

## Reviewer Assignments
Reviewer Name | Assigned Focus Area
--- | ---
Tan | Logic / Correctness
Druv | Unit Tests
Durga | Design / Maintainability
Tan | Edge Cases / Robustness

## Checklist Compliance
Confirm reviewers used required checklists:
- Code Review Checklist
- Unit Test Review Checklist
- Severity classification applied correctly
