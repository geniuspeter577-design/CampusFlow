# Reflection: geniuspeter577-design

**One mistake I verified:** In the Understanding Check, Q4, I answered A (append the note anyway) for a resolved ticket. That was wrong. I ran the app, tried to add a note to resolved ticket T006, and it said "Notes can only be added to open or in_progress tickets." The correct answer is C (reject until reopened).

**One thing I learned:** .lower() and .casefold() both make text lowercase, but casefold() is stronger. "Straße".casefold() gives "strasse", and .lower() does not. I use casefold() in search because it is safer for comparing text.

**One improvement from code review:** In Q6, I answered A (approve because it runs). The better action is B: ask for focused tests and reasoning. A change to validation with no negative-case tests should not be approved just because it runs.
