
QUESTIONS = [
    {
        "question": "An open ticket has no assignee. What should happen if someone tries to move it to in_progress?",
        "options": {
            "A": "Assign it automatically to the first available person.",
            "B": "Reject the change and preserve all ticket data.",
            "C": "Move it to in_progress anyway.",
            "D": "Delete the ticket."
        },
        "answer": "B",
    },
    {
        "question": "What should the resolution percentage be when there are zero tickets?",
        "options": {
            "A": "100%",
            "B": "Undefined, causing the app to crash.",
            "C": "0%",
            "D": "50%"
        },
        "answer": "C",
    },
    {
        "question": "A user searches for title='wifi', category='Network', and status='open'. Which tickets should appear?",
        "options": {
            "A": "Every ticket with 'wifi' in its title.",
            "B": "Only tickets matching all three filters.",
            "C": "Tickets matching any one filter.",
            "D": "Only open Network tickets, regardless of title."
        },
        "answer": "B",
    },
    {
        "question": "What should happen when someone tries to add a note to a resolved ticket?",
        "options": {
            "A": "Add the note immediately.",
            "B": "Change the ticket to open automatically.",
            "C": "Reject the note until the ticket is reopened.",
            "D": "Delete the existing notes."
        },
        "answer": "C",
    },
    {
        "question": "A JSON file contains two tickets with the same ID. What should the loader do?",
        "options": {
            "A": "Silently merge the tickets.",
            "B": "Load both tickets.",
            "C": "Reject the load without changing the current in-memory data.",
            "D": "Delete one duplicate and continue."
        },
        "answer": "C",
    },
    {
        "question": "A pull request changes validation logic but adds no tests for invalid inputs. What is the best review response?",
        "options": {
            "A": "Approve immediately because the code runs.",
            "B": "Request focused negative-case tests and an explanation of the behavior.",
            "C": "Rewrite the entire project.",
            "D": "Ignore validation because users should enter correct data."
        },
        "answer": "B",
    },
]
