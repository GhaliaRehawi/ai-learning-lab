# Week 1 — Reflection (in progress)

**Theme:** Python fluency + Git hygiene
**Sessions logged:** Day 1 (2026-04-29)

## What I covered

- Python: functions with type hints, `with open`, `csv.DictReader`,
  `defaultdict`, comprehensions for filter/map/group, dict comprehensions,
  `if __name__ == "__main__"` guard, `sys.argv`.
- Refactoring: turned a messy procedural CSV script into a small, typed,
  testable function.
- Testing: pytest fundamentals — `assert`, `pytest.approx`, fixtures,
  `tmp_path`, `parametrize`, mutation testing as a sanity check.
- Repo discipline: started `ai-learning-lab` with structured folders for
  exercises, tests, and a learning journal.

## What went well

- Caught my own uncertainty on `parametrize` and flagged it instead of
  pretending it worked. That's the right reflex.
- After seeing the foundations once, I wrote idiomatic code on the second
  attempt (`defaultdict`, `with open`, `csv.DictReader`, type hints).
- Reached for the right structural patterns (filter, group, aggregate)
  from the start, even when I couldn't yet write the syntax fluently.

## Where I struggled

- Translating a correct mental plan into working Python syntax. Gap is in
  *writing*, not *reading*.
- Test infrastructure correctness — bugs accumulated in the *plumbing*
  (fixture wiring, assert form, parametrize syntax) rather than in the
  test content itself.
- Mixed mental models: pandas-style indexing applied to plain Python lists.

## Recurring weak areas to watch

1. Test infrastructure correctness — `assert` paired with `approx`,
   fixture consumption, `parametrize` shape. Run a mutation check on every
   new test suite.
2. Distinguishing list, dict, set, and generator semantics; not blurring
   their APIs.
3. Pandas-flavored thinking creeping into pure-Python code.

## Cross-cutting takeaways

- A test you can't trust is worse than no test. Mutation-check new
  suites by breaking the production code and confirming the tests fail.
- Default arguments and comprehension brackets are quiet correctness
  hazards in Python — worth memorizing the traps before they show up
  in real research code.
- Idiomatic Python is shorter and more declarative than the procedural
  version. When you find yourself writing a manual init-then-append
  pattern, reach for `defaultdict`. When you find yourself writing
  `for k in d: out[k] = f(d[k])`, reach for a dict comprehension.

## Open items / next session

- Day 2: hands-on Git — `rebase -i`, `cherry-pick`, and recovery
  scenarios on this repo.
- Small repo hygiene fixes:
  - Add `.gitignore` (`.idea/`, `__pycache__/`, `.pytest_cache/`,
    `.venv/`).
  - Pin `pytest>=8.0` in `requirements.txt`.
  - Decide whether `mistakes-to-revist.md/` should be a single file
    `mistakes-to-revisit.md` (also fix typo).
  - Remove stale comment at top of `tests/test_gene_means.py`.
