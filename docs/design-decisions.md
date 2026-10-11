# CampusFlow Design Decisions

## 1. Separation of responsibilities
- tickets.py is responsible for ticket creation and validation.
- workflow.py handles ticket assignment, status updates, and the open-ticket queue.
- reports.py calculates ticket summaries.
- storage.py handles persistence.
- main.py connects application logic to the command-line interface.

## 2. Workflow functions
Assignment, status management, and queue ordering are separate functions so each responsibility can be tested independently.

## 3. Status validation
Only open, in_progress, and resolved are accepted.
An unassigned ticket cannot move to in_progress.
A resolved ticket must be reopened before it can move to another status.

## 4. Queue ordering
Only open tickets are included.
Tickets are ordered critical, high, medium, then low.
Tickets with equal priority are ordered by their numeric ID.

## 5. Reporting
The reporting function returns a dictionary of totals rather than printing directly.
This separates business logic from presentation and makes the function easier to test.

## 6. Testing
Python unittest is used to test normal behavior, validation failures, queue ordering, and empty inputs.
