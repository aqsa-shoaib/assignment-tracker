# Student Assignment Tracker

A desktop assignment tracker built with Python and Tkinter. It helps students organize their schoolwork, view upcoming deadlines, and keep track of completed assignments.

## Features

- Add assignments with a subject, title, and due date
- View assignments sorted by deadline, with unfinished tasks listed first
- Mark assignments as completed or undo completion
- See when an unfinished assignment is overdue
- Delete assignments you no longer need
- Save assignments automatically in a local JSON file
- Use the app offline without installing extra Python packages

## Requirements

- Python 3.9 or newer
- Tkinter (included with most Windows and macOS Python installations)

## Run the application

Download the repository, open a terminal in the project folder, and run:

```bash
python app.py
```

On some macOS or Linux systems, use `python3 app.py`.

## How to use

1. Enter a subject, assignment name, and due date in `YYYY-MM-DD` format (for example, `2027-02-10`).
2. Click **Add assignment** to save it.
3. Select an assignment and click **Mark complete / Undo** to update its status.
4. Select an assignment and click **Delete selected** to remove it.
5. Close the window when you're done. Your assignments will still be there next time.

Assignments are stored in `assignments.json`, which is automatically created when you add your first assignment. This file is excluded from Git so personal schoolwork doesn't get uploaded.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Built with

- **Python** for application logic
- **Tkinter** for the graphical interface
- **JSON** for local data storage
- **unittest** for testing

## Project structure

```text
student-assignment-tracker/
├── app.py
├── tracker.py
├── README.md
├── .gitignore
└── tests/
    └── test_tracker.py
```
