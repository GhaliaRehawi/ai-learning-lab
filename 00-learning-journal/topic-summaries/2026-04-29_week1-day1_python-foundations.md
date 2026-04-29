# Week 1, Day 1 — Python Foundations for ML

**Date:** 2026-04-29
**Session focus:** Functions, file I/O, dict/list idioms, refactoring, pytest basics.

## Topic

Python fluency for ML work: writing clean, idiomatic Python and turning messy
scripts into testable functions. First contact with pytest infrastructure.

## Coding lessons

### Filtering and grouping
- Filter a list of dicts with a comprehension, not pandas-style indexing:
  `[g for g in genes if g["is_tf"]]`. Plain lists do not support boolean indexing.
- The four core idioms that cover most data wrangling in pure Python:
  - filter: `[x for x in items if cond(x)]`
  - map: `[f(x) for x in items]`
  - group: `defaultdict(list)` + single pass + `.append`
  - dict transform: `{k: f(v) for k, v in d.items()}`

### Dicts vs lists
- `list.append(x)` vs `dict[key] = value`. Dicts have no `.append`.
- `defaultdict(list)` and `defaultdict(dict)` remove the
  `if key not in d: d[key] = ...` boilerplate.
- Convert `defaultdict` back to plain `dict` at API boundaries:
  `return dict(res)`.

### File I/O and CSV
- Always use `with open(path, "r") as f:` — auto-closes even on errors.
- `csv.DictReader` yields each row as a dict keyed by header. Every value is
  a string — convert numerics explicitly with `float(...)`.
- For nested aggregation, build `{outer_key: {inner_key: value}}` with
  `defaultdict(dict)`.

### Functions and structure
- Type hints on signatures: `def f(path: str) -> dict[str, float]:`. Not
  enforced at runtime; for readers and tools.
- `if __name__ == "__main__":` guard — code runs only when the file is
  executed directly, not on import.
- Replace `for k in d: out[k] = f(d[k])` with a dict comprehension. Signals
  "transformation," not "control flow."

### pytest basics
- Test files: `test_*.py`. Test functions: `def test_*()`. Use plain
  `assert`.
- `pytest.approx(expected)` only works inside `assert x == pytest.approx(...)`.
  Bare `pytest.approx(...)` is a silent no-op.
- `tmp_path` fixture gives each test a fresh temporary directory — prefer it
  over committing fixture files.
- A fixture only runs when its name appears as a parameter of the test.
- `@pytest.mark.parametrize("name1,name2", [(...), (...)])` — first arg is
  the parameter name(s), and those names must appear in the test signature.
- **Mutation check:** after writing tests, deliberately break the production
  code and confirm tests fail. The single best habit for trusting your tests.
- `np.allclose(...)` for arrays, `pytest.approx(...)` for scalars. Never use
  `==` on floats.

## 3 Recall questions

1. What is the difference between `defaultdict(list)` and `dict()` when you
   do `d[key].append(x)` on a key that doesn't exist yet?
2. Why is `pytest.approx(result, expected)` on its own (no `assert`)
   a no-op, and what's the correct usage?
3. What does the `tmp_path` fixture do, and why is it preferable to
   committing fixture CSV files into the repo?

## Weak points and mistakes to focus on

1. **Bare `pytest.approx` without `assert`** — silent no-op. Always pair
   `assert` with `approx`. Run a mutation check on every new test suite.
2. **Defining a fixture but not consuming it** in the test signature. Pytest
   only injects fixtures whose names appear as parameters.
3. **`parametrize` parameter-name confusion** — the first argument is the
   parameter name(s) of the test function, not a filename or metadata.
4. **Pandas-style boolean indexing on plain lists** —
   `genes["is_tf" == True]` does not filter; use a comprehension.
5. **`list.append` vs `dict[key] = value`** — keep the APIs separate.
6. **Mutable default arguments** (`def f(x, items=[])`) — defaults are
   evaluated once at function definition. Use `None` + sentinel instead.
7. **Generator vs list vs set comprehensions** —
   `(...)` is a generator (lazy, single-pass), not a set.
8. **Forgetting to convert CSV string values to `float`** before arithmetic.

## Next session

Day 2 — Git workflow practice. Hands-on `rebase -i`, `cherry-pick`, and a
recovery scenario on the `ai-learning-lab` repo. Goal: move a misplaced
commit between branches without help.
