# Week 1 — Reflection (in progress)

**Theme:** Python fluency + Git hygiene
**Sessions logged:** Day 1 (2026-04-29), Day 2 (2026-04-30)

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

## Day 2 update — Git mental model

### What I covered

- Git's data model: blobs, trees, commits, tags as content-hashed
  objects.
- Commit = snapshot pointer + parent pointer(s) + metadata. Not a diff.
- Branch = a tiny text file at `.git/refs/heads/<name>` containing
  one SHA. Slashes in branch names are real directory separators.
- HEAD = a pointer to the current branch (or a raw SHA when detached).
- How every operation maps onto "create new objects, move pointers":
  commit, checkout, merge, rebase, cherry-pick, reset.
- Interactive rebase verbs (`pick`, `reword`, `edit`, `squash`,
  `fixup`, `drop`) and the control trio (`--continue`, `--skip`,
  `--abort`).
- Old commits are never destroyed by rebase/reset — they linger in
  the object database, recoverable via `git reflog`.
- Commit-message hygiene: describe changes, not filenames.

### What went well

- Got the core mental model on the first explanation: commits as
  snapshot pointers, branches as pointer files, HEAD as a pointer to
  the current branch.
- Predicted correctly that `git checkout main` moves HEAD but does
  not touch branch refs.
- Reasoned correctly about why rebased commits get new SHAs (parent
  pointers and metadata change, and SHAs hash all of it).

### Where I struggled

- Dropped the suffix on branch paths (`.../heads/feature` instead of
  `.../heads/feature/git-practice`). Branch names are paths.
- Multi-step exercise lost two of three commits silently because I
  didn't verify each step. The rebase that followed had nothing to
  squash, so the practice didn't happen.
- Skipped the prediction step on one of the questions. Predictions
  are where the model gets built; running commands without predicting
  is a verification, not a learning, exercise.
- Didn't know `git rebase --abort`. Should have learned the abort
  command before the forward command.

### Open items / next session

- Week 1, Day 3: Python packaging and imports — modules vs packages,
  `__init__.py`, the import search path, and a refactor of the repo
  so `from exercises.gene_means import gene_means` is robust.
- Rebase + cherry-pick fluency to be picked up in real workflow over
  the next 7 weeks rather than via more synthetic drills.
- Small repo hygiene fixes still pending:
  - Add `.gitignore` (`.idea/`, `__pycache__/`, `.pytest_cache/`,
    `.venv/`).
  - Pin `pytest>=8.0` in `requirements.txt`.
  - Decide whether `mistakes-to-revist.md/` should be a single file
    `mistakes-to-revisit.md` (also fix typo).
  - Remove stale comment at top of `tests/test_gene_means.py`.
