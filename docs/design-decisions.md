# CampusFlow Design Decisions

## 1. Separation of responsibilities

- `tickets.py` validates ticket input, calculates priority, generates IDs, and creates tickets.
- `workflow.py` handles assignment, status changes, and the open-ticket queue.
- `storage.py` loads and saves ticket data in JSON format.
- `reports.py` generates ticket summary reports.
- `main.py` provides the command-line interface and connects the modules.
- `tests/` contains automated unit tests for the application.

## 2. Ticket validation

Titles must contain non-whitespace text and are trimmed before storage.
Categories are normalized to Network, Hardware, Software, or Other.
Urgency is normalized to lowercase and must be low, medium, or high.
Affected users must be a positive integer; booleans are not accepted.

## 3. Priority rules

- High urgency and at least 10 affected users: critical.
- High urgency or at least 10 affected users: high.
- Medium urgency or at least 3 affected users: medium.
- Otherwise: low.

The rules are evaluated from highest to lowest priority.

## 4. Ticket IDs

Ticket IDs use the format `T001`, `T002`, and so on.
New IDs are generated from the largest valid existing numeric ID.

## 5. Workflow

Tickets begin with open status and no assignee.
A ticket must be assigned before moving to `in_progress`.
Resolved tickets must be reopened before further changes.
The open queue contains only open tickets and sorts by priority, then numeric ID.

## 6. Persistence and reporting

Ticket records are persisted as JSON. A missing data file starts with an empty
ticket list, while malformed data must produce a clear error rather than
silently discarding saved tickets.

Reports count tickets by status and priority and include the total ticket count.

## 7. Testing

The application uses Python's `unittest` framework to test validation,
priority calculation, ticket creation, workflow rules, persistence, and reports.
