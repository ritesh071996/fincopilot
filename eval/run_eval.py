"""Evaluation harness — runs the question set and reports the metrics that
define success (docs/01-goals.md): accuracy, citation coverage, refusal
correctness. Accuracy uses an LLM-as-judge.

Run:  python -m eval.run_eval
"""

from pathlib import Path

import yaml

from app.gateway import llm
from app.rag.answer import answer_question

QUESTIONS_FILE = Path(__file__).parent / "questions.yaml"

JUDGE_SYSTEM = (
    "You are a strict grader. Compare a CANDIDATE answer to a REFERENCE answer. "
    "Reply with exactly one word: PASS if the candidate conveys the same key "
    "facts as the reference (wording may differ), otherwise FAIL."
)


def judge(question: str, reference: str, candidate: str) -> bool:
    prompt = (
        f"Question: {question}\n\n"
        f"REFERENCE answer: {reference}\n\n"
        f"CANDIDATE answer: {candidate}\n\n"
        "Does the candidate match the reference? Reply PASS or FAIL."
    )
    verdict = llm.complete(prompt, system=JUDGE_SYSTEM).strip().upper()
    return verdict.startswith("PASS")


def main() -> None:
    questions = yaml.safe_load(QUESTIONS_FILE.read_text(encoding="utf-8"))

    acc_total = acc_pass = 0          # accuracy (answerable only)
    cite_total = cite_ok = 0          # citation coverage (answerable only)
    ref_total = ref_ok = 0            # refusal correctness (should_refuse only)

    for i, q in enumerate(questions, start=1):
        result = answer_question(q["question"])

        if q["should_refuse"]:
            ref_total += 1
            ok = result.refused
            ref_ok += int(ok)
            print(f"[{i:02d}] REFUSE  {'OK ' if ok else 'BAD'}  {q['question'][:60]}")
        else:
            cite_total += 1
            cite_ok += int(bool(result.citations) and not result.refused)

            acc_total += 1
            passed = (not result.refused) and judge(q["question"], q["expected"], result.answer)
            acc_pass += int(passed)
            print(f"[{i:02d}] ANSWER  {'PASS' if passed else 'FAIL'}  {q['question'][:60]}")

    print("\n================ SCORECARD ================")
    pct = lambda a, b: f"{(100 * a / b):.0f}%" if b else "n/a"
    print(f"Accuracy (LLM-judge):   {acc_pass}/{acc_total}  ({pct(acc_pass, acc_total)})")
    print(f"Citation coverage:      {cite_ok}/{cite_total}  ({pct(cite_ok, cite_total)})")
    print(f"Refusal correctness:    {ref_ok}/{ref_total}  ({pct(ref_ok, ref_total)})")


if __name__ == "__main__":
    main()
