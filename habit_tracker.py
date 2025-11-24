"""
Simplified Habit Tracker (interactive only, no external dependencies)
---------------------------------------------------------------
Python version: 3.7+

Usage:
  python habit_tracker.py

Major components:
- Data model: Habit (dataclass)
- Persistence: load/save from JSON
- Core logic: creation, deletion, completion
- Analytics module: longest streak computation (purely functional)
- User interface: simple interactive command-line interface (CLI)
- Fixture generator: produces reproducible example data for testing

Commands inside the interactive menu:
  list        → list all habits
  add         → create a new habit (daily or weekly)
  delete      → delete a habit
  complete    → mark a habit as completed on a date
  analytics   → show longest streaks for all habits  
  init        → initialize example habits.json with 5 predefined habits
  exit        → quit the program

Predefined example data: 5 habits (Meditate, Run, Read, Grocery, Call Mom)
Each has 4 weeks of completions for testing and demonstration.



"""
# Libraries to import
import json
import os
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional

# Filename used for storing all habits persistently as JSON.
HABITS_FILENAME = "habits.json"
DATE_FMT = "%Y-%m-%d" # Standardized date format (ISO-like) used across the application for consistency.

@dataclass
class Habit:
    name: str # The descriptive name of the habit (e.g., "Run", "Meditate").
    periodicity: str  # 'daily' or 'weekly'
    completions: List[str]

# Persistence layer (JSON storage)
def load_habits(filename: str = HABITS_FILENAME) -> List[Habit]: 
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Habit(**x) for x in data]

def save_habits(habits: List[Habit], filename: str = HABITS_FILENAME) -> None: #Serialize and save all habits to a JSON file; 
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([asdict(h) for h in habits], f, indent=2)

# Core logic (management functions)
def get_habit_by_name(habits: List[Habit], name: str) -> Optional[Habit]:
    for h in habits:
        if h.name == name:
            return h
    return None

def create_habit(habits: List[Habit], name: str, periodicity: str) -> List[Habit]: # Creates a new habit and returns an updated list.
    if get_habit_by_name(habits, name):
        raise ValueError(f"Habit '{name}' already exists.")
    if periodicity not in ("daily", "weekly"):
        raise ValueError("Periodicity must be 'daily' or 'weekly'.")
    return habits + [Habit(name, periodicity, [])]

def delete_habit(habits: List[Habit], name: str) -> List[Habit]: # Deletes a habit by name.
    return [h for h in habits if h.name != name]

def mark_complete(habits: List[Habit], name: str, when: date) -> List[Habit]: # Records the completion of a habit and asks for the date of completion
    found = get_habit_by_name(habits, name)
    if not found:
        raise ValueError(f"Habit '{name}' not found.")
    iso = when.strftime(DATE_FMT)
    if iso in found.completions:
        return habits
    new_habits = []
    for h in habits:
        if h.name == name:
            new_habits.append(Habit(h.name, h.periodicity, h.completions + [iso]))
        else:
            new_habits.append(h)
    return new_habits

# Analytics module
def _iso_to_date(s: str) -> date:
    return datetime.strptime(s, DATE_FMT).date() #  Converts an ISO date string into a `datetime.date` object.

def _sorted_dates(h: Habit) -> List[date]:
    return sorted(map(_iso_to_date, h.completions)) # Return all completion dates of a habit sorted chronologically

def _longest_run_for_dates(dates: List[date], step: int) -> int: # Computes the longest consecutive streak of dates separated by a step.
    if not dates:
        return 0
    streak, best = 1, 1
    for a, b in zip(dates, dates[1:]):
        if (b - a).days == step:
            streak += 1
        else:
            best = max(best, streak)
            streak = 1
    return max(best, streak)

def longest_run_for_habit(h: Habit) -> int:
    dates = _sorted_dates(h)
    step = 1 if h.periodicity == "daily" else 7 #For daily habits, step = 1 day; for weekly, step = 7 days.
    return _longest_run_for_dates(dates, step)

def longest_run_all(habits: List[Habit]) -> Dict[str, int]: #Computes the longest run streak for all defined habits
    return {h.name: longest_run_for_habit(h) for h in habits}

# Fixtures (test data)
def _date_range(start: date, days: int) -> List[date]: #Returns a list of consecutive days starting from 'start'
    return [start + timedelta(days=i) for i in range(days)]

def _week_dates(start: date, weeks: int) -> List[date]: #Returns a list of weekly intervals starting from 'start'.
    return [start + timedelta(weeks=i) for i in range(weeks)]

def init_fixtures(filename: str = HABITS_FILENAME) -> None: # Creates predefined example habits and stores them to disk.
    today = date.today() #The date ranges are relative to the current day. This data serves as a test fixture for validation or demonstration purposes.
    start = today - timedelta(days=27)  #four weeks of completion data for each of the data created

    med_dates = [d.strftime(DATE_FMT) for i, d in enumerate(_date_range(start, 28)) if i not in (5, 12, 20)]
    run_dates = [d.strftime(DATE_FMT) for i, d in enumerate(_date_range(start, 28)) if i % 2 == 0]
    read_dates = [d.strftime(DATE_FMT) for i, d in enumerate(_date_range(start, 28)) if i % 3 != 0]
    grocery_dates = [d.strftime(DATE_FMT) for d in _week_dates(start, 4)]
    call_dates = [d.strftime(DATE_FMT) for i, d in enumerate(_week_dates(start + timedelta(days=1), 4)) if i != 2]
    habits = [ # Generates five habits: three daily and two weekly
        Habit("Walk 10.000 steps", "daily", med_dates), 
        Habit("Drink water", "daily", run_dates),
        Habit("Read", "daily", read_dates),
        Habit("Groceries", "weekly", grocery_dates),
        Habit("Call Mom", "weekly", call_dates),
    ]
    save_habits(habits, filename)

# Interactive CLI (Command Line Interface). 
# Available commands: list -(display all tracked habits), add (add a new habit), complete (mark a habit as completed and request the date of completion), analytics (compute longest run streaks), init (create example data), exist (terminate the program). 
def main():
    habits = load_habits()
    while True:
        print("\nOptions: list, add, delete, complete, analytics, init, exit") # Menu
        c = input("> ").strip()
        if c == "list": # List all habits with their completion count.
            for h in habits:
                print(f"{h.name} ({h.periodicity}) - completions: {len(h.completions)}")
        elif c == "add": # Create a new habit.
            name = input("Name: ")
            periodicity = input("Periodicity (daily/weekly): ")
            try:
                habits = create_habit(habits, name, periodicity)
                save_habits(habits)
                print("Habit created.")
            except ValueError as e:
                print(e)
        elif c == "delete": # Delete a habit by name.
            name = input("Name: ")
            habits = delete_habit(habits, name)
            save_habits(habits)
            print("Habit deleted (if it existed).")
        elif c == "complete":  # Mark a habit as completed at a given date.
            name = input("Name: ")
            d = input("Date (YYYY-MM-DD): ")
            try:
                when = datetime.strptime(d, DATE_FMT).date()
                habits = mark_complete(habits, name, when)
                save_habits(habits)
                print("Completion recorded.")
            except Exception as e:
                print("Error:", e)
        elif c == "analytics": # Display longest streaks for all habits.
            results = longest_run_all(habits)
            print("Longest streaks:")
            for name, streak in results.items():
                print(f"{name}: {streak}")
        elif c == "init":  # Generate example dataset.
            init_fixtures()
            habits = load_habits()
            print("Fixtures initialized.")
        elif c == "exit":   # Terminate the program.
            break
        else:
            print("Unknown command.")

#Program entry point
if __name__ == "__main__":
    main()