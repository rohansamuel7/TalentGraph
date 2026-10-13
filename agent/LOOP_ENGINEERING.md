# Engineering Loop

`READ → PLAN → IMPLEMENT → TEST → EVALUATE → FIX → RETEST → DOCUMENT → NEXT TASK`

1. Read `AGENTS.md` and relevant project documentation.
2. Select one defined task from `TASKS.md`.
3. State measurable acceptance criteria.
4. Implement the smallest coherent change.
5. Run relevant automated tests.
6. Inspect actual failure output; identify the likely root cause.
7. Apply a focused correction and rerun tests.
8. Make at most three focused repair attempts per failure.
9. If unresolved, record the blocker and stop the task.
10. On success, run applicable regression checks.
11. Update `TASKS.md`, `PROGRESS.md`, and `VALIDATION.md`; record significant decisions.
12. Start another task only after the current criteria are met.

Never claim unexecuted tests passed, silently skip failures, hide blockers, endlessly refactor working code, or change major architecture without approval.
