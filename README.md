# Observer Log

A simple observation management application written in Python using procedural programming.

## Features

* Add observations with target name, date, exposure, and notes
* Display all saved observations
* Search observations by target name
* Delete observations by ID
* Store records persistently in an SQLite database
* Export observations to CSV
* Validate numerical exposure values using NumPy
* Handle invalid input and common database or file errors

## Technologies

* Python
* SQLite
* NumPy
* CSV

## Installation

Install Python 3, then install the required dependency:

```bash
python -m pip install -r requirements.txt
```

## Run the application

```bash
python Observer-log.py
```

## Data storage

The application creates `observer_log.db` automatically in the current working directory.

Use the menu to add, view, search, or delete observations and export records to `observations.csv`.

## Project structure

```text
Observer-Log/
├── Observer-log.py
├── README.md
├── requirements.txt
└── .gitignore
```

The database and CSV export are generated when the application runs.

## Programming concepts

* Functions
* Lists and tuples
* Input validation
* SQLite database operations
* CSV file handling
* NumPy numerical validation
* Exception handling

## License

This project is intended for learning and educational use.

"# Dornika.13888" 
