"""A desktop assignment tracker built with Python and Tkinter."""

import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from tracker import (
    create_assignment,
    delete_assignment,
    load_assignments,
    save_assignments,
    sort_assignments,
    toggle_completed,
)


class AssignmentTracker:
    """Display assignments and handle actions in the desktop window."""

    def __init__(self, root):
        self.root = root
        self.root.title("Student Assignment Tracker")
        self.root.geometry("780x520")
        self.root.minsize(660, 420)
        try:
            self.assignments = load_assignments()
        except (OSError, ValueError) as error:
            messagebox.showerror("Unable to load assignments", str(error))
            self.assignments = []

        self.subject = tk.StringVar()
        self.title = tk.StringVar()
        self.due_date = tk.StringVar()
        self.status = tk.StringVar()

        self.build_interface()
        self.refresh_list()

    def build_interface(self):
        """Create the assignment form, table, and action buttons."""
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Student Assignment Tracker", font=("Arial", 19, "bold")).pack(anchor="w")
        ttk.Label(container, text="Keep track of your coursework and upcoming deadlines.").pack(anchor="w", pady=(4, 15))

        form = ttk.Frame(container)
        form.pack(fill="x", pady=(0, 12))
        fields = [("Subject", self.subject, 18),
                  ("Assignment", self.title, 29),
                  ("Due date (YYYY-MM-DD)", self.due_date, 16)]
        for column, (label, variable, width) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=0, column=column, sticky="w", padx=(0, 10))
            ttk.Entry(form, textvariable=variable, width=width).grid(row=1, column=column, sticky="ew", padx=(0, 10), pady=(4, 0))
        form.columnconfigure(1, weight=1)
        ttk.Button(form, text="Add assignment", command=self.add_assignment).grid(row=1, column=3, sticky="ew")

        table_frame = ttk.Frame(container)
        table_frame.pack(fill="both", expand=True)
        columns = ("subject", "assignment", "deadline", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        for name, heading, width in [
            ("subject", "Subject", 140), ("assignment", "Assignment", 255),
            ("deadline", "Due date", 120), ("status", "Status", 105)
        ]:
            self.table.heading(name, text=heading)
            self.table.column(name, width=width, minwidth=90)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.bind("<Double-1>", lambda event: self.change_status())

        actions = ttk.Frame(container)
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Mark complete / Undo", command=self.change_status).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Delete selected", command=self.remove_assignment).pack(side="left")
        ttk.Label(actions, textvariable=self.status).pack(side="right")

    def save(self):
        """Write the latest assignments to disk and report save errors."""
        try:
            save_assignments(self.assignments)
            return True
        except OSError as error:
            messagebox.showerror("Unable to save", str(error))
            return False

    def refresh_list(self):
        """Update the table and the completed assignment count."""
        for item in self.table.get_children():
            self.table.delete(item)
        for task in sort_assignments(self.assignments):
            if task["completed"]:
                status = "Completed"
            elif task["due_date"] < date.today().isoformat():
                status = "Overdue"
            else:
                status = "Pending"
            self.table.insert("", "end", iid=str(task["id"]),
                              values=(task["subject"], task["title"], task["due_date"], status))
        completed = sum(task["completed"] for task in self.assignments)
        self.status.set(f"{completed}/{len(self.assignments)} completed")

    def add_assignment(self):
        """Add a new assignment from the form."""
        try:
            create_assignment(self.assignments, self.subject.get(), self.title.get(), self.due_date.get().strip())
        except ValueError as error:
            messagebox.showwarning("Check your assignment", str(error))
            return
        self.save()
        self.subject.set("")
        self.title.set("")
        self.due_date.set("")
        self.refresh_list()

    def selected_id(self):
        """Return the selected assignment ID, or show a helpful message."""
        selection = self.table.selection()
        if not selection:
            messagebox.showinfo("Select an assignment", "Click an assignment in the list first.")
            return None
        return int(selection[0])

    def change_status(self):
        """Mark a selected assignment complete or switch it back to pending."""
        assignment_id = self.selected_id()
        if assignment_id is None:
            return
        toggle_completed(self.assignments, assignment_id)
        self.save()
        self.refresh_list()

    def remove_assignment(self):
        """Delete a selected assignment after confirmation."""
        assignment_id = self.selected_id()
        if assignment_id is None:
            return
        if messagebox.askyesno("Delete assignment", "Delete the selected assignment?"):
            delete_assignment(self.assignments, assignment_id)
            self.save()
            self.refresh_list()


if __name__ == "__main__":
    window = tk.Tk()
    AssignmentTracker(window)
    window.mainloop()
