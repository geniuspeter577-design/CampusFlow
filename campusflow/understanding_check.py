"""Scoring and question flow for the Engineering Understanding Check."""

from campusflow.cli import ask_valid
from campusflow.question_bank import QUESTIONS

LETTERS = ("a", "b", "c", "d")


def score_answers(questions, answers):
    """One point per correct submitted answer. Returns 0..len(questions)."""
    if len(answers) != len(questions):
        raise ValueError("Need exactly one answer per question.")
    score = 0
    for question, answer in zip(questions, answers):
        if isinstance(answer, str) and answer.strip().upper() == question["answer"]:
            score += 1
    return score


def format_question(question):
    """Question text plus its A/B/C/D options as one string."""
    lines = [f"{question['id']}. {question['text']}"]
    for letter, text in question["options"].items():
        lines.append(f"  {letter}. {text}")
    return "\n".join(lines)


def run_check(questions=QUESTIONS, input_func=input, output_func=print):
    """Ask every question (re-asking on bad input). Returns (score, answers)."""
    answers = []
    for question in questions:
        output_func(format_question(question))
        answers.append(ask_valid("Your answer (A/B/C/D): ", LETTERS,
                                 input_func, output_func).upper())
    score = score_answers(questions, answers)
    output_func(f"Final score: {score}/{len(questions)}")
    return score, answers
