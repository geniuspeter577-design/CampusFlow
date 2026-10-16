"""Small, testable helpers for the command-line menu."""


def ask_valid(prompt, allowed, input_func=input, output_func=print):
    """Keep asking until the answer (trimmed, lowercase) is in `allowed`."""
    while True:
        answer = input_func(prompt).strip().casefold()
        if answer in allowed:
            return answer
        options = ", ".join(a if a else "(Enter to skip)" for a in allowed)
        output_func(f"Invalid choice. Options: {options}")


def format_ticket_row(ticket):
    """One readable line for search results."""
    return (
        f"{ticket['id']} | {ticket['title']} | {ticket['category']} | "
        f"{ticket['priority']} | {ticket['status']} | "
        f"{ticket['assigned_to'] or 'unassigned'}"
    )
