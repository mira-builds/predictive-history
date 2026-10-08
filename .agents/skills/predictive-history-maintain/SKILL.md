---
name: predictive-history-maintain
description: Maintain Predictive History public content and tooling through scoped edits, appropriate checks, verified GitHub identity, and explicitly authorized publication. Use for repository maintenance or GitHub publishing; ordinary reading does not activate it.
---

# Predictive History Maintain

All project paths are relative to the repository root, three directories above this skill. Read root `AGENTS.md`, `docs/contracts/public-repo-contract.md`, and `docs/contracts/export-contract.md` for the controlling public boundaries.

Recover the requested endpoint: edited files, a local commit, a remote push, a pull request, and deployment are distinct outcomes. Carry explicit authorization forward without expanding it. Guidance grants no permission to publish, communicate, change access, or deploy.

Inspect the exact repository root, branch, remote, and working-tree changes. Preserve unrelated work and source originals. Name the candidate and excluded paths before staging. When copying, compare tracked, untracked, and relevant ignored files; inspect ignore rules rather than assuming every excluded file is disposable. Exclude credentials, private records, machine paths, caches, and inherited Git history from public candidates.

Use the existing Python project and CLI. Set `PYTHONPATH=src` for source execution. Run focused tests while editing; before publication run `python -m pytest`, `python -m civ_ph.cli validate`, and `python -m civ_ph.cli index --check`. Validation regenerates supported public reports, so inspect its changes. Passing checks establish technical consistency, not scholarly approval or audience reach.

Before each GitHub mutation, verify the effective account for that tool. Publication targets `mira-builds/predictive-history`; verify the destination, author and committer attribution, submitting account, and actual push credential separately. Do not switch global credentials or reuse another lane's authentication. If a connector fails, inspect already-authorized CLI access; distinguish account mismatch, authentication failure, missing files, and visibility. Keep secrets and raw authentication errors out of output.

Stage only reviewed candidate paths and inspect the staged diff. Confirm that committed bytes match validation evidence. Publish only the authorized branch and refspec; do not silently force-push, merge, rebase, create a PR, or deploy. When an operation's result is uncertain, read back the destination before retrying.

After an external write, freshly verify the exact remote SHA or provider artifact identity and content. Report local edits, validation, commit, verified push, and hosting separately, with the actual delivered link. Account or transport mismatch blocks that action while independently useful preparation may continue. The skill needs no Mira Core runtime, private registry, or installed hooks.
