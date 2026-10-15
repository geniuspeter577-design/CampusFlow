# CampusFlow

CampusFlow is a Python command-line helpdesk ticket management system designed to help campus technical support teams manage, assign, track, and resolve support requests.

## Features

- **Ticket management:** Create and list support tickets.
- **Assignment:** Assign tickets to support personnel.
- **Status tracking:** Update ticket statuses and manage ticket workflows.
- **Ticket notes:** Add notes to tickets and preserve them across save and load operations.
- **Search and filtering:** Search tickets by title and filter using supported ticket fields.
- **Priority queue:** View open tickets in priority order.
- **Ticket details:** View information about individual tickets.
- **Reports:** View ticket counts, priority summaries, unresolved tickets, resolution percentage, and category breakdowns.
- **Validation:** Reject invalid ticket data and workflow operations.

## Requirements

- Python 3
- Git (optional, for cloning and contributing)

No third-party packages are required for the current standard-library-based application and tests.

## Getting Started

Clone the repository and enter the project directory:

```bash
git clone https://github.com/ireubencodes/CampusFlow.git
cd CampusFlow
```

Run the application:

```bash
python main.py
```

Follow the interactive menu to select an available operation.

## Running Tests

Run the complete test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

The tests cover ticket validation, notes, storage, workflows, search, and reports.

## Project Structure

```text
CampusFlow/
├── main.py
├── campusflow/
│   ├── reports.py
│   ├── search.py
│   ├── storage.py
│   └── workflow.py
└── tests/
    ├── test_notes.py
    ├── test_reports.py
    ├── test_search.py
    ├── test_storage.py
    ├── test_tickets.py
    └── test_workflow.py
```

- `main.py`: Command-line interface and menu.
- `campusflow/reports.py`: Ticket reporting and summary calculations.
- `campusflow/search.py`: Ticket search and filtering.
- `campusflow/storage.py`: Ticket data persistence and loading/saving.
- `campusflow/workflow.py`: Ticket assignment, status changes, queue handling, and note operations.
- `tests/`: Automated tests for the application's functionality.

## Contributing

1. Start from the latest `main` branch.
2. Create a separate branch for your task.
3. Make focused changes and run the test suite.
4. Commit and push your branch.
5. Open a pull request into `main` for review.

## License

No license has been specified yet.
