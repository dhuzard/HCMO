> Status: AI-assisted draft generated from repository structure and metadata. Requires human review before being treated as authoritative.

# Agent Guide

Instructions for AI coding agents working on **dhuzard/HCMO**. Read this
before proposing changes.

## What you may safely modify

- Source code under `<src / package dir>` with accompanying tests
- Documentation in `docs/` and `README.md`
- Tests under `tests/`
- Configuration you fully understand

You may edit these freely as long as tests pass and the change is scoped.

## What you must NOT modify without human approval

- `LICENSE`, `CITATION.cff`, `CREDITS.md` (attribution & legal)
- Anything under data/ or model artefacts (provenance-sensitive)
- CI/CD secrets, workflow permissions, or release automation
- Scientific analysis logic — flag changes for human review
- Public API signatures without a deprecation note

## Commands to run before proposing changes

```bash
# Install
pip install -e .            # adjust to this repo

# Lint / type-check (if configured)
# ruff check . ; mypy .

# Tests — must pass before you open a PR
pytest
```

Do not propose a change that leaves the test suite red.

## Working agreement

- Keep changes small and reviewable; one concern per PR.
- Explain *why*, not just *what*, in the PR description.
- Never commit secrets or `.env` files; never paste secrets into prompts.
- If a change touches scientific correctness, data, or attribution, mark it
  **requires human review** and do not self-merge.
- Prefer additive documentation (see the Trust Pack) over silent behavioural
  changes.

## Forbidden actions

- Force-pushing, rewriting history, or deleting branches
- Disabling tests or CI to make a change pass
- Introducing network calls to undisclosed endpoints
- Fabricating results, citations, or contributor roles

## Review status

- Last human review: <date> by <name>
