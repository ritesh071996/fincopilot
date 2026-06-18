"""The LangGraph agent — the orchestration brain.

agent.py defines the stateful graph:

    retrieve -> draft -> compliance-review -> (amend -> re-review)* -> answer

with loop caps so it can't run forever. Built in Week 4-5.
"""
