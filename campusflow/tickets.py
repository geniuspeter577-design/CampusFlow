# title validation
def validate_title(title):
    if not title.strip():
        raise ValueError("Title cannot be blank.")

    return title.strip()


# category validation
def validate_category(category):
    category = category.strip().capitalize()

    allowed_categories = ["Network", "Hardware", "Software", "Other"]
    if category not in allowed_categories:
        raise ValueError("Invalid Category")

    return category 


# Urgency validation
def validate_urgency(urgency):
    urgency = urgency.strip().lower()

    allowed_urgencies = ["low", "medium", "high"]

    if urgency not in allowed_urgencies:
        raise ValueError("Invalid urgency.")

    return urgency


# Affected users validation
def validate_affected_users(affected_users):
    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError("Affected users must be a positive whole number.")

    return affected_users


# Priority validation
def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


# Ticket ID generation
def generate_ticket_id(tickets):
    if not tickets:
        return "T001"

    numbers = [int(ticket["id"][1:]) for ticket in tickets]
    next_number = max(numbers) + 1

    return f"T{next_number:03d}"


def create_ticket(title, category, urgency, affected_users, tickets):
    title = validate_title(title)
    category = validate_category(category)
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    priority = calculate_priority(urgency, affected_users)
    ticket_id = generate_ticket_id(tickets)

    ticket = {
        "id": ticket_id,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None
    }

    return ticket