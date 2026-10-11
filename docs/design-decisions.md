# CampusFlow Design Decisions

## 1. Project Purpose

CampusFlow is a Python command-line application for managing campus technical support tickets.

## 2. Ticket Data Structure

We will store tickets in a list of dictionaries.

Each ticket will contain:
- id
- title
- category
- urgency
- affected_users
- priority
- status
- assigned_to

## 3. Module Responsibilities

- main.py: Displays the menu and handles user interaction.
- campusflow/tickets.py: Validates ticket details, calculates priority, generates IDs, and creates tickets.
- campusflow/workflow.py: Handles assignment, status transitions, and the work queue.
- campusflow/storage.py: Loads tickets from JSON and saves tickets to JSON.
- campusflow/reports.py: Generates ticket statistics.

## 4. Validation and Errors

Business logic will validate inputs and raise appropriate exceptions for invalid operations.

The CLI will catch these errors and display understandable messages.

## 5. Testing

Business logic functions should be testable without interactive terminal input.

We will use Python's unittest framework.

## 6. Persistence

Tickets will be stored in a JSON file.

The application will load saved tickets at startup and save successful changes.

Missing storage files will start with an empty ticket collection. Malformed JSON must produce a clear error without silently deleting existing data.

## 7. Collaboration

Each fellow will work on an assigned feature branch, write tests, and open a pull request.

Each fellow must review and approve the other fellow's pull request before merging.