# Repository Custodianship

This repository is **custodied by the AI assistant (Codex)** on behalf of the owner.
The custodian is allowed to perform routine maintenance tasks; it must not perform
destructive or ownership-changing actions without explicit confirmation.

## Routine actions the custodian MAY do without asking

- Open / update / merge **Draft** pull requests from feature branches
- Push feature branches (`codex/feat-*`, `codex/fix-*`, `codex/chore-*`) to `origin`
- Run `pytest`, `npm run build`, `npm run lint` and report results
- Add / update `.gitignore`, PR templates, CI workflow, this document
- `git rm --cached <file>` for files that should no longer be tracked
  (after listing them for the owner to review)
- Create annotated tags for releases (e.g. `v0.1.0`) and push them
- Triage issues: label, link related PRs, request more info

## Actions that REQUIRE explicit owner approval

- Force-push to any branch
- Push directly to `main` (must always go through a PR)
- Delete a remote branch that has been merged but is < 7 days old
- Delete or rewrite git history (`git rebase` of shared branches, filter-repo)
- Merge a PR that changes authentication, authorization, secrets handling,
  billing, or data-export endpoints
- Publish a release / GitHub Release
- Add or change GitHub Actions that have `permissions: write-all`
- Sign commits on the owner's behalf

## Actions the custodian will NEVER do

- Read, store, log, or transmit the owner's GitHub PAT, passwords, API keys,
  cookies, or session tokens. The owner must configure credentials in their
  own credential manager.
- Send messages to third parties (Discord, DingTalk, email, etc.) on the
  owner's behalf.
- Push to a different repository than `https://github.com/Zcx-BaixiaoBai/GE-paw.git`.
- Force-push or amend commits the owner authored.

## Branch strategy

- `main` is protected. Direct pushes are blocked; changes must land via PR.
- Feature work: `codex/<type>-<short-slug>` (types: `feat`, `fix`, `chore`, `docs`, `refactor`, `perf`, `test`).
- Long-running integration: `develop` (created only if the owner opts in).
- Releases: tagged `vMAJOR.MINOR.PATCH` on `main`.

## Commit message style

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat(scope): short summary`
- `fix(scope): short summary`
- `chore(scope): short summary`
- `refactor(scope): short summary`

Subject line <= 72 chars, imperative mood, no trailing period.

## Reporting cadence

After any action, the custodian reports in chat:

1. What it did (one-line)
2. The PR / commit / branch involved
3. Any verification it ran (test / build result)
4. Anything the owner needs to review or approve
