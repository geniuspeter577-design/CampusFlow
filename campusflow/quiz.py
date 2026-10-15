
from campusflow.quiz_questions import QUESTIONS


def collect_answer(question, input_fn=input, output_fn=print):
    """Ask a question until the user enters A, B, C, or D."""
    output_fn(f"\n{question['question']}")

    for letter, option in question["options"].items():
        output_fn(f"  {letter}. {option}")

    while True:
        answer = input_fn("Your answer (A/B/C/D): ").strip().upper()
        if answer in question["options"]:
            return answer
        output_fn("Invalid choice. Please enter A, B, C, or D.")


def collect_explanation(question_number, input_fn=input, output_fn=print):
    """Collect a short explanation for a submitted answer."""
    while True:
        explanation = input_fn(
            f"Briefly explain your reasoning for question {question_number}: "
        ).strip()

        if explanation:
            return explanation

        output_fn("Please enter a short explanation.")


def run_quiz(input_fn=input, output_fn=print):
    """Run the six-question understanding check and return the results."""
    score = 0
    explanations = []

    output_fn("\n=== CampusFlow Engineering Understanding Check ===")

    for number, question in enumerate(QUESTIONS, start=1):
        output_fn(f"\nQuestion {number} of {len(QUESTIONS)}")

        answer = collect_answer(question, input_fn, output_fn)

        if answer == question["answer"]:
            score += 1
            output_fn("Correct.")
        else:
            output_fn(f"Not quite. The correct answer is {question['answer']}.")

        if number in (2, 5):
            explanation = collect_explanation(
                number, input_fn, output_fn
            )
            explanations.append({
                "question_number": number,
                "explanation": explanation,
            })

    output_fn(f"\nFinal score: {score}/{len(QUESTIONS)}")
    output_fn("\nYour explanations:")
    for item in explanations:
        output_fn(
            f"Question {item['question_number']}: {item['explanation']}"
        )

    return {
        "score": score,
        "total": len(QUESTIONS),
        "explanations": explanations,
    }
