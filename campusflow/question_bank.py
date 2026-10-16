"""The six Understanding Check questions. Data only - no scoring here."""

QUESTIONS = [
    {
        "id": "Q1",
        "text": "Ticket T001 is open and unassigned. A user tries to move it to in_progress.",
        "options": {"A": "Accept", "B": "Reject and preserve all data",
                    "C": "Resolve it automatically", "D": "Remove ticket"},
        "answer": "B",
    },
    {
        "id": "Q2",
        "text": "The app has zero tickets. What should resolution percentage display?",
        "options": {"A": "Crash", "B": "100%", "C": "0%",
                    "D": "Divide by one without explanation"},
        "answer": "C",
    },
    {
        "id": "Q3",
        "text": "Filter title='wifi', category='Network', status='open'. Which records should match?",
        "options": {"A": "Any record matching one filter",
                    "B": "Only records matching all supplied filters",
                    "C": "All network records", "D": "All open records"},
        "answer": "B",
    },
    {
        "id": "Q4",
        "text": "A resolved ticket receives 'Add note'. What should happen?",
        "options": {"A": "Append anyway", "B": "Delete old notes",
                    "C": "Reject until reopened", "D": "Change status silently"},
        "answer": "C",
    },
    {
        "id": "Q5",
        "text": "The JSON file includes two tickets with the same ID. What should load do?",
        "options": {"A": "Keep both", "B": "Replace memory with duplicates",
                    "C": "Reject the load without changing current memory",
                    "D": "Rename IDs silently"},
        "answer": "C",
    },
    {
        "id": "Q6",
        "text": "A PR changes validation but has no negative-case tests. Best review action?",
        "options": {"A": "Approve because it runs",
                    "B": "Request focused tests and reasoning",
                    "C": "Merge immediately", "D": "Ask AI to approve it"},
        "answer": "B",
    },
]
