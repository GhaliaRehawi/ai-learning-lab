# Week 1, Day 2 — Git mental model: commits, branches, HEAD

**Date:** 2026-04-30
**Session focus:** What Git actually stores, and what every operation
really does to that data.

## Topic

Most Git frustration comes from treating Git as magic. It isn't — it's a
small, mechanical system built on three precise concepts. Once those click,
every command (commit, checkout, branch, rebase, cherry-pick, reset, merge)
becomes "create new objects and move pointers."

### Git's data model — the four object types

Everything in `.git/objects/` is one of:

| Object  | What it represents                                                 |
|---------|--------------------------------------------------------------------|
| blob    | the raw bytes of a single file                                     |
| tree    | a directory listing — names + permissions + pointers to blobs/trees |
| commit  | a snapshot pointer + metadata                                      |
| tag     | a named, signed reference to a commit                              |

Each object is identified by the SHA-1 of its contents. Same content =
same SHA, always.

### What a commit really is

A commit is a small text object containing:

- a pointer (SHA) to **one tree** — a full snapshot of the project at that
  moment
- pointers (SHAs) to its **parent commit(s)** — usually one, two for
  merges, zero for the very first commit
- author name/email/timestamp
- committer name/email/timestamp
- a commit message

**Crucially: a commit is NOT a diff.** It points to a complete snapshot.
Diffs are *computed* by comparing two commits' trees. This is why
`cherry-pick` and `rebase` work — they compute the diff between a commit
and its parent, then re-apply that diff somewhere else and create a new
commit (with a new SHA, because parents/timestamps differ).

### What a branch really is

A branch is **a tiny text file** at `.git/refs/heads/<branch-name>`
containing **one SHA** — the commit at the tip of the branch.

```
$ cat .git/refs/heads/main
f209a8b3bfc496dda6b8dbb96edf98ccf23e5b82
```

Creating a branch = copying ~41 bytes. Deleting a branch = removing
~41 bytes. The commits themselves are not duplicated.

**Branch names are filesystem paths.** `feature/git-practice` is stored
as `.git/refs/heads/feature/git-practice` — a directory `feature/`
containing a file `git-practice`. This is why naming conventions like
`feature/`, `bugfix/`, `release/` group cleanly when you list refs.

### What HEAD really is

`HEAD` is a tiny file at `.git/HEAD` whose contents are usually:

```
ref: refs/heads/main
```

It says: "the current branch is `main`." When you `git checkout other`,
HEAD is rewritten to `ref: refs/heads/other`.

When HEAD instead contains a raw SHA (no `ref:` line), you're in
**detached HEAD** state — standing on a specific commit, not on any
branch. Committing while detached creates orphan commits findable only
via `git reflog`.

### Every operation, decoded

Once you internalize the model, operations become mechanical:

- `git commit` → create a new commit object pointing at the current tree
  with HEAD's branch as parent; rewrite that branch's ref file to the new
  SHA.
- `git checkout other` → rewrite `.git/HEAD` to point at `other`; update
  working directory to match `other`'s tree. **Branch refs are not
  touched.**
- `git merge other` → create a commit with two parents; advance the
  current branch's pointer to it.
- `git rebase main` → for each commit on the current branch since
  divergence, recompute its diff against `main`'s tip and create a new
  commit with a new SHA. Move the current branch's ref to the last new
  commit. **Old commits remain in the object database** until garbage
  collection (default ~30 days), recoverable via `git reflog`.
- `git cherry-pick <sha>` → take the diff of `<sha>` against its parent;
  apply on top of the current commit; create a new commit with a new SHA.
- `git reset --hard <sha>` → rewrite the current branch's ref to `<sha>`;
  reset working directory.

The rule that ties this together: **only branch refs and HEAD move. Old
commits are never destroyed by these operations** — they're just
unreferenced, and survive until garbage collection. `git reflog` is your
safety net for recovering anything that "disappeared."

### Interactive rebase — what it actually does

`git rebase -i <base>` opens an editor listing every commit between
`<base>` and HEAD, with a verb in front of each:

| verb     | effect                                                             |
|----------|--------------------------------------------------------------------|
| `pick`   | keep as-is                                                         |
| `reword` | keep, but edit the message                                         |
| `edit`   | pause at this commit so you can amend it                           |
| `squash` | combine into the previous commit, merge messages                   |
| `fixup`  | like squash but discard this commit's message                      |
| `drop`   | remove the commit entirely (or just delete the line)               |

Save and close → Git replays the list in order, creating new commits.
Three control commands govern the process:

- `git rebase --continue` — after resolving conflicts in a paused rebase
- `git rebase --skip` — drop the current commit and continue
- `git rebase --abort` — return to exactly the state before the rebase
  started

### Commit message hygiene

Commit messages describe **changes**, not filenames. `test_gene_means.py`
as a message tells future-you nothing. Convention:

- First line ≤ 50 chars, imperative mood
- Optional prefix: `feat:`, `fix:`, `tests:`, `refactor:`, `docs:`,
  `journal:`
- Optional blank line + body for context

Example: `tests: parametrize constant-value test, add negative case`

This pays off in `git log`, `git blame`, `git bisect`, and code review.

## Coding lessons

- A commit is a snapshot pointer + parent pointer(s) + metadata, hashed.
  Not a diff.
- A branch is a 41-byte file containing one SHA. Slashes in branch names
  become real directories on disk.
- HEAD is a pointer to the current branch (or a raw SHA in detached
  state).
- `git checkout` moves HEAD only. Branch refs change only when you commit
  or run a history-rewriting operation (`reset`, `rebase`, `merge`,
  `push -f`).
- Rebase creates new commits with new SHAs — even if the diff is
  identical — because parents/timestamps/messages may differ, and SHAs
  hash *all* of that.
- Old commits aren't destroyed by rebase or reset; they linger in the
  object database. `git reflog` finds them.
- Use `--force-with-lease` (not `--force`) when pushing a rebased
  branch. Never rebase shared/public branches.
- Commit messages describe the change, not the filename.

## 3 Recall questions

1. After `git checkout main`, which files inside `.git/` change, and
   which files do not? Be specific.
2. After `git rebase -i main` rewrites three commits on a feature branch,
   are the original three commits gone? If not, where are they, and how
   can you find them?
3. You're on `feature/x`, three commits ahead of `main`. The middle
   commit belongs on `main` instead. Sketch the strategy (no exact
   commands needed) to move it.

## Weak points and mistakes to focus on

1. **Branch names are paths.** `feature/git-practice` lives at
   `.git/refs/heads/feature/git-practice`, not `.git/refs/heads/feature`.
   Stop dropping the suffix when reasoning about branch refs.
2. **Predict before running.** Skipping the prediction step on Git
   exercises throws away the entire learning value. The model is built
   by being wrong on paper before being wrong on disk.
3. **Verify each step before chaining.** Today's mess started because
   three intended commits silently became one and the rebase had nothing
   to squash. Run `git log --oneline -1` after every commit during
   multi-step exercises.
4. **Commit messages must describe changes**, not filenames. Three
   commits named `test_gene_means.py` in a row is a code-review smell.
5. **Don't know `git rebase --abort`.** Always learn the abort/recovery
   commands before learning the forward operation. Worth memorizing the
   trio: `--continue`, `--skip`, `--abort`.

## Next session

Week 1, Day 3 — Python packaging and imports. Modules vs packages,
`__init__.py`, the import search path, and refactoring the repo so
`from exercises.gene_means import gene_means` works robustly regardless
of where pytest is invoked.
