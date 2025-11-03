[README.txt](https://github.com/user-attachments/files/23306182/README.txt)
# Habit Tracker Application

## Overview

This Python-based Habit Tracker provides a minimal yet complete implementation of a habit management system.  
It demonstrates clean software design, functional programming in analytics, and persistence using the JSON format.  

The system is **self-contained**, relies only on Python's standard library, and can be executed in any environment supporting Python 3.7 or later.  

## Features

- Persistent storage using `habits.json`
- Command-line interface (CLI) for direct interaction
- Predefined test data generation (5 habits over 4 weeks)
- Functional analytics module:
  - List all habits
  - List habits by periodicity (daily / weekly)
  - Compute longest run streak across all habits
  - Compute longest run streak for a specific habit

## System Requirements

- **Python version:** 3.7 or higher  
- **Operating system:** Cross-platform (Windows, macOS, Linux)  
- **Dependencies:** None beyond the Python standard library

## Installation Instructions

1. Clone or download the project to your local system:
   ```bash
   git clone https://github.com/[your-username]/habit-tracker.git
   cd habit-tracker
