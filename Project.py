#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import sqlite3
import numpy as np
from datetime import datetime


DATABASE_NAME = "observer_log.db"
CSV_NAME = "observations.csv"


# -------------------------
# Database
# -------------------------

def connect_database():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    """Create the observations table if it does not exist."""
    with connect_database() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                observation_date TEXT NOT NULL,
                exposure REAL NOT NULL,
                notes TEXT
            )
        """)


# -------------------------
# Input validation
# -------------------------

def get_non_empty_text(message):
    """Read a non-empty text value."""
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Input cannot be empty. Please try again.")


def get_exposure():
    """Read and validate a finite, non-negative exposure value."""
    while True:
        raw_value = input("Exposure: ").strip()

        try:
            value = float(raw_value)

            # NumPy validates that the value is finite.
            if not np.isfinite(value):
                print("Exposure must be a finite number.")
                continue

            if value < 0:
                print("Exposure cannot be negative.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


def get_observation_date():
    """Read a date in YYYY-MM-DD format."""
    while True:
        value = input(
            "Observation date (YYYY-MM-DD, blank for today): "
        ).strip()

        if not value:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")


# -------------------------
# Add observation
# -------------------------

def add_observation():
    """Collect and save a new observation."""
    print("\n--- Add Observation ---")

    target = get_non_empty_text("Target name: ")
    observation_date = get_observation_date()
    exposure = get_exposure()
    notes = input("Notes (optional): ").strip()

    try:
        with connect_database() as connection:
            connection.execute("""
                INSERT INTO observations
                    (target, observation_date, exposure, notes)
                VALUES (?, ?, ?, ?)
            """, (target, observation_date, exposure, notes))

        print("Observation added successfully!")

    except sqlite3.Error as error:
        print(f"Database error: {error}")


# -------------------------
# Show observations
# -------------------------

def show_observations():
    """Display all saved observations."""
    print("\n--- All Observations ---")

    try:
        with connect_database() as connection:
            cursor = connection.execute("""
                SELECT id, target, observation_date, exposure, notes
                FROM observations
                ORDER BY id
            """)

            observations = cursor.fetchall()

        if not observations:
            print("No observations found.")
            return

        for observation in observations:
            observation_id, target, date, exposure, notes = observation

            print(f"\nID: {observation_id}")
            print(f"Target: {target}")
            print(f"Date: {date}")
            print(f"Exposure: {exposure:g}")
            print(f"Notes: {notes or 'None'}")

    except sqlite3.Error as error:
        print(f"Database error: {error}")


# -------------------------
# Search observations
# -------------------------

def search_observations():
    """Search observations by target name."""
    print("\n--- Search Observations ---")

    keyword = get_non_empty_text("Enter target name to search: ")

    try:
        with connect_database() as connection:
            cursor = connection.execute("""
                SELECT id, target, observation_date, exposure, notes
                FROM observations
                WHERE target LIKE ?
                ORDER BY id
            """, (f"%{keyword}%",))

            results = cursor.fetchall()

        if not results:
            print("No matching observations found.")
            return

        for observation in results:
            observation_id, target, date, exposure, notes = observation

            print(f"\nID: {observation_id}")
            print(f"Target: {target}")
            print(f"Date: {date}")
            print(f"Exposure: {exposure:g}")
            print(f"Notes: {notes or 'None'}")

    except sqlite3.Error as error:
        print(f"Database error: {error}")


# -------------------------
# Delete observation
# -------------------------

def delete_observation():
    """Delete an observation by its ID."""
    print("\n--- Delete Observation ---")

    raw_id = input("Enter observation ID: ").strip()

    try:
        observation_id = int(raw_id)

        if observation_id <= 0:
            print("ID must be a positive integer.")
            return

    except ValueError:
        print("Please enter a valid integer ID.")
        return

    try:
        with connect_database() as connection:
            cursor = connection.execute(
                "DELETE FROM observations WHERE id = ?",
                (observation_id,)
            )

            if cursor.rowcount == 0:
                print("No observation found with that ID.")
            else:
                print("Observation deleted successfully!")

    except sqlite3.Error as error:
        print(f"Database error: {error}")


# -------------------------
# Export to CSV
# -------------------------

def export_to_csv():
    """Export all observations to a CSV file."""
    print("\n--- Export to CSV ---")

    try:
        with connect_database() as connection:
            cursor = connection.execute("""
                SELECT id, target, observation_date, exposure, notes
                FROM observations
                ORDER BY id
            """)

            observations = cursor.fetchall()

        with open(
            CSV_NAME,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow([
                "ID",
                "Target",
                "Observation Date",
                "Exposure",
                "Notes"
            ])

            writer.writerows(observations)

        print(f"Export completed: {CSV_NAME}")

    except (sqlite3.Error, OSError) as error:
        print(f"Export error: {error}")


# -------------------------
# Menu
# -------------------------

def show_menu():
    """Display the main menu."""
    print("\n========== OBSERVER LOG ==========")
    print("1. Add observation")
    print("2. Show all observations")
    print("3. Search observations")
    print("4. Delete observation")
    print("5. Export observations to CSV")
    print("0. Exit")
    print("==================================")


def main():
    """Run the application."""
    create_table()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_observation()

        elif choice == "2":
            show_observations()

        elif choice == "3":
            search_observations()

        elif choice == "4":
            delete_observation()

        elif choice == "5":
            export_to_csv()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from the menu.")


if __name__ == "__main__":
    main()

