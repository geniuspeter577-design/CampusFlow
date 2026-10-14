# CampusFlow Baseline Check

## Automated tests
- Command: `python -m unittest discover -s tests -v`
- Result: 46 tests passed.

## Manual checks
- Ran `python main.py` successfully.
- High urgency with 9 affected users produced high priority.
- High urgency with 10 affected users produced critical priority.
- High urgency with 2 affected users produced high priority.
- Medium urgency with 2 affected users produced medium priority.
- The application saved ticket records in `tickets.json`.
- Ticket IDs continued from T001 through T005 in the observed data.

## Initial observations
- Local runtime data should not be committed to the repository.
- Existing ticket fields include ID, title, category, urgency, affected users,
  priority, status, and assignee.
- Ticket notes are implemented as a list of strings and covered by tests.
- Notes survive JSON save/load round trips.
- Mentor audit feedback: pending confirmation; not recorded yet.

## Next steps
- Confirm remaining assignment requirements and mentor feedback.
- Integrate the ticket-note CLI commands with Engineer B's work.
- Complete the remaining tests and documentation.
- Review the combined changes before opening pull requests.
