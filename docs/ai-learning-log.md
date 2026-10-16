# AI learning log

## Engineer: geniuspeter577-design

### Cycle 1: casefold vs lower in ticket search

**Concept gap (my own words):** `.lower()` and `.casefold()` were already in the code, and I did not know how they differ.

**Exact question asked:** Compare casefold and lower for search; suggest test cases but do not implement my project.

**AI guidance (summary):** Both make text lowercase, but `casefold()` is stronger and made for comparing text without case. For example, German `ß` becomes `ss`. For plain English both work, and `casefold()` is the safer standard for search. Suggested tests: `WI-FI` vs `wi-fi`, mixed case, `wifi` must not match `wi-fi`, empty search means no filter.

**Tiny unrelated experiment:** I ran this in the terminal:

    word = "Straße"
    print(word.lower(), word.casefold())             # straße strasse
    print("STRASSE".lower() == word.lower())         # False
    print("STRASSE".casefold() == word.casefold())   # True
    print("WI-FI".casefold() == "wi-fi".casefold())  # True
    print("wifi" in "wi-fi down")                    # False

**Independent verification:** I wrote `tests/test_search_casefold.py` (2 tests) against my real `search_tickets` function. Both pass. Commit 8e46897.

**Final engineering decision:** Keep `casefold()` in `campusflow/search.py`. The two tests now guard this behaviour, including that punctuation must match.
