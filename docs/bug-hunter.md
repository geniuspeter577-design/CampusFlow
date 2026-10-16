# Bug-hunter write-up: geniuspeter577-design

## Edge case 1: boolean affected_users in a saved file

**Initial state:** A tickets.json file with one ticket, T001, where `affected_users` is `true` (a boolean) and not a number.

**Input:** `load_validated_tickets(path)` is called on that file.

**Expected result:** The load is rejected with a `ValueError`, because `True` behaves like the number 1 in Python (isinstance(True, int) is True) and must not be accepted as a count of users.

**Actual result:** A `ValueError` is raised, and the bad ticket is not loaded.

**Test name:** `test_boolean_affected_users_in_file_is_rejected_on_load` in `tests/test_bug_hunter.py`

**Code change:** None needed in this commit. The test was added in commit 871ccb0 to guard this behaviour.

## Edge case 2: note ID gap

**Initial state:** A ticket with two notes, N001 and N003 (N002 is missing).

**Input:** `next_note_id(ticket)` is called.

**Expected result:** `N004`. Counting the notes (2) and adding 1 would give N003, which already exists and would create a duplicate ID.

**Actual result:** `N004`. The function uses the highest existing number, not the count.

**Test name:** `test_next_note_id_uses_highest_number_not_count` in `tests/test_bug_hunter.py`

**Code change:** None needed in this commit. The test was added in commit 871ccb0 to guard this behaviour.
