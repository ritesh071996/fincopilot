"""Evaluation harness — runs the question set and reports the metrics that
define success (see docs/01-goals.md):

    - answer accuracy        (LLM-as-judge vs. expected answer)
    - citation coverage      (did it cite a valid source?)
    - hallucinated numbers   (any number not in a source -> hard fail)
    - refusal correctness    (did it refuse the should_refuse questions?)

Usage:
    python -m eval.run_eval

Built in Week 8-9. This stub documents the intended interface.
"""

from pathlib import Path

import yaml

QUESTIONS_FILE = Path(__file__).parent / "questions.yaml"


def load_questions() -> list[dict]:
    return yaml.safe_load(QUESTIONS_FILE.read_text(encoding="utf-8"))


def main() -> None:
    questions = load_questions()
    print(f"Loaded {len(questions)} eval questions.")
    # TODO (Week 8-9): for each question -> call the agent -> judge ->
    #   aggregate metrics -> print a scorecard.
    raise SystemExit("Eval harness not implemented yet (Week 8-9).")


if __name__ == "__main__":
    main()
