# CampusFlow Next

A Python command-line helpdesk for campus technical support. Staff register
problems (Wi-Fi, laptops, software, learning tools), track them, leave
follow-up notes, search tickets and read reports.

Python standard library only. No external packages.

## Run the app

    python main.py

## Run the tests (works from a fresh clone)

    git clone https://github.com/geniuspeter577-design/CampusFlow.git
    cd CampusFlow
    git checkout fix/campusflow-next
    python -m unittest discover -s tests -v

## Menu

    1. Create ticket
    2. List tickets
    3. Assign ticket
    4. Update ticket status
    5. Show open queue
    6. Show report
    7. Add follow-up note
    8. View ticket notes
    9. Search tickets
    10. Search tickets (sorted by priority)
    11. Engineering Understanding Check
    0. Save and exit

## Business rules

- Category: Network, Hardware, Software or Other. Urgency: low, medium or high.
- affected_users must be a strictly positive whole number (no 0, negatives,
  decimals, text or True/False).
- Priority: critical when urgency is high AND affected_users >= 10; otherwise
  high when urgency is high OR affected_users >= 10; otherwise medium when
  urgency is medium OR affected_users >= 3; otherwise low.
- Status flow: open -> in_progress -> resolved; a resolved ticket can be
  reopened to open. A ticket must be assigned before it can be in_progress.
- A resolved ticket cannot be assigned or receive notes until it is reopened.
- Rejected actions never change any ticket data.
- Open queue (option 5): only OPEN tickets, ordered critical > high > medium >
  low, then by numeric ticket number (T2 before T10).

## Notes

- A note is {note_id, author, message} with per-ticket IDs N001, N002, ...
- Only open or in_progress tickets accept notes.
- Author cannot be blank. Message must be 5-300 characters after trimming.
- A rejected note does not use up a note ID. Notes are kept through
  resolve and reopen.

## Search (options 9 and 10)

- Title: case-insensitive substring match (WI-FI matches wi-fi).
- Optional category, status and priority filters. Press Enter to skip one.
- All supplied filters must match (AND). Invalid choices ask again.
- Search never changes tickets. Option 10 sorts the results by priority, then
  by numeric ticket number. It does not replace the open queue.

## Report (option 6)

Total tickets, counts by status, priority and category, unresolved (open +
in_progress), resolved, and resolution percentage (resolved / total x 100).
No tickets gives 0%. Reopened tickets count by their CURRENT status.

## Data file format (tickets.json)

A JSON list. Each ticket is an object:

    {
      "id": "T001",
      "title": "Wi-Fi down",
      "category": "Network",
      "urgency": "high",
      "affected_users": 12,
      "priority": "critical",
      "status": "open",
      "assigned_to": null,
      "notes": [
        {"note_id": "N001", "author": "Mentor A", "message": "Router reboot attempted"}
      ]
    }

On start-up the WHOLE file is validated first: structure, required keys,
unique ticket IDs, valid category/urgency/status, priority matching the rule,
and note shapes with unique note IDs per ticket. If anything is wrong the app
refuses to load, prints the reason and does not change the file.

## Understanding Check (option 11)

Six multiple-choice questions (A/B/C/D) about how this app behaves, scored
0-6. You then explain two answers in your own words. Explanations are saved
to docs/understanding-check-notes.md for mentor discussion and are never
auto-graded.

## Project layout

- campusflow/ : tickets, workflow, notes, search, reports, storage,
  validation, cli helpers, question bank, understanding check, explanations
- tests/ : unittest test files
- docs/ : baseline-check.md, design-decisions.md
