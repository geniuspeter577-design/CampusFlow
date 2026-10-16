"""Learner explanations for the Understanding Check.

Saved for mentor discussion. They are never auto-graded.
"""

from datetime import date
from pathlib import Path

from campusflow.question_bank import QUESTIONS
from campusflow.understanding_check import run_check

NOTES_PATH = Path("docs") / "understanding-check-notes.md"
MIN_EXPLANATION = 10
EXPLAIN_COUNT = 2


def ask_explanation(prompt, input_func=input, output_func=print):
    """Keep asking until the explanation has enough characters."""
    while True:
        text = input_func(prompt).strip()
        if len(text) >= MIN_EXPLANATION:
            return text
        output_func(f"Please write at least {MIN_EXPLANATION} characters.")


def save_explanations(entries, path=NOTES_PATH, today=None):
    """Append (question_id, answer, text) entries to a markdown note."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    today = today or date.today().isoformat()
    lines = [f"\n## Understanding Check - {today}\n"]
    for question_id, answer, text in entries:
        lines.append(f"- **{question_id}** (answered {answer}): {text}")
    with open(path, "a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def run_check_with_explanations(questions=QUESTIONS, input_func=input,
                                output_func=print, notes_path=NOTES_PATH):
    """Run the quiz, then collect and save explanations. Returns (score, entries)."""
    score, answers = run_check(questions, input_func, output_func)
    output_func(f"Now explain {EXPLAIN_COUNT} of your answers in your own words.")
    entries = []
    for question, answer in list(zip(questions, answers))[:EXPLAIN_COUNT]:
        text = ask_explanation(
            f"Why did you choose {answer} for {question['id']}? ",
            input_func, output_func)
        entries.append((question["id"], answer, text))
    save_explanations(entries, notes_path)
    output_func(f"Saved explanations to {notes_path} for mentor discussion.")
    return score, entries
