"""Tests for the assignment tracker data functions."""

import tempfile
import unittest
from pathlib import Path

from tracker import (
    create_assignment,
    delete_assignment,
    load_assignments,
    save_assignments,
    sort_assignments,
    toggle_completed,
    valid_date,
)


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.assignments = []

    def test_add_assignment(self):
        task = create_assignment(self.assignments, "Math", "Homework", "2027-02-10")
        self.assertEqual(task["id"], 1)
        self.assertFalse(task["completed"])

    def test_blank_fields_are_rejected(self):
        with self.assertRaises(ValueError):
            create_assignment(self.assignments, "", "Homework", "2027-02-10")

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValueError):
            create_assignment(self.assignments, "Math", "Homework", "2027-02-30")

    def test_date_format_is_checked(self):
        self.assertTrue(valid_date("2027-02-10"))
        self.assertFalse(valid_date("02/10/2027"))

    def test_sort_by_due_date(self):
        create_assignment(self.assignments, "Math", "Later", "2027-03-01")
        create_assignment(self.assignments, "English", "Sooner", "2027-02-01")
        self.assertEqual(sort_assignments(self.assignments)[0]["title"], "Sooner")

    def test_completed_tasks_are_last(self):
        create_assignment(self.assignments, "Math", "Complete", "2027-01-01")
        create_assignment(self.assignments, "English", "Pending", "2027-03-01")
        toggle_completed(self.assignments, 1)
        self.assertEqual(sort_assignments(self.assignments)[0]["title"], "Pending")

    def test_toggle_completed(self):
        create_assignment(self.assignments, "Math", "Homework", "2027-02-10")
        toggle_completed(self.assignments, 1)
        self.assertTrue(self.assignments[0]["completed"])
        toggle_completed(self.assignments, 1)
        self.assertFalse(self.assignments[0]["completed"])

    def test_delete(self):
        create_assignment(self.assignments, "Math", "Homework", "2027-02-10")
        delete_assignment(self.assignments, 1)
        self.assertEqual(self.assignments, [])

    def test_ids_are_unique(self):
        first = create_assignment(self.assignments, "Math", "One", "2027-02-10")
        second = create_assignment(self.assignments, "Math", "Two", "2027-02-11")
        self.assertNotEqual(first["id"], second["id"])

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "assignments.json"
            create_assignment(self.assignments, "Math", "Homework", "2027-02-10")
            save_assignments(self.assignments, path)
            self.assertEqual(load_assignments(path), self.assignments)

    def test_first_launch_without_file(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_assignments(Path(directory) / "missing.json"), [])


if __name__ == "__main__":
    unittest.main()
