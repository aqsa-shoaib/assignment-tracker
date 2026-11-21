"""Store and organize assignments for the Student Assignment Tracker."""

import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path(__file__).with_name("assignments.json")
DATE_FORMAT = "%Y-%m-%d"


def valid_date(date_text):
    """Return True when the date exists and uses YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_text, DATE_FORMAT).strftime(DATE_FORMAT) == date_text
    except ValueError:
        return False


def load_assignments(file_path=DATA_FILE):
    """Load saved assignments, or return an empty list if no file exists."""
    if not file_path.exists():
        return []
    with file_path.open("r", encoding="utf-8") as file:
        assignments = json.load(file)
    if not isinstance(assignments, list):
        raise ValueError("Saved assignments must be a list.")
    return assignments


def save_assignments(assignments, file_path=DATA_FILE):
    """Save assignments to a JSON file."""
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(assignments, file, indent=2)


def sort_assignments(assignments):
    """Show unfinished assignments first, ordered by nearest deadline."""
    return sorted(assignments, key=lambda task: (task["completed"], task["due_date"], task["subject"].lower()))


def create_assignment(assignments, subject, title, due_date):
    """Validate the form and add a new assignment with a unique ID."""
    subject = subject.strip()
    title = title.strip()
    if not subject or not title:
        raise ValueError("Enter a subject and assignment name.")
    if not valid_date(due_date):
        raise ValueError("Enter a valid date in YYYY-MM-DD format.")
    next_id = max((task["id"] for task in assignments), default=0) + 1
    task = {"id": next_id, "subject": subject, "title": title,
            "due_date": due_date, "completed": False}
    assignments.append(task)
    return task


def toggle_completed(assignments, assignment_id):
    """Switch an assignment between pending and completed."""
    for task in assignments:
        if task["id"] == assignment_id:
            task["completed"] = not task["completed"]
            return
    raise ValueError("Assignment not found.")


def delete_assignment(assignments, assignment_id):
    """Remove an assignment by its ID."""
    for index, task in enumerate(assignments):
        if task["id"] == assignment_id:
            del assignments[index]
            return
    raise ValueError("Assignment not found.")
