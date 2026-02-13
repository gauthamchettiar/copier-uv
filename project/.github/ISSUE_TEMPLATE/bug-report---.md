---
name: "Bug report \U0001F41E"
about: Create a bug report
labels: bug

---

## Short summary
A one-line summary of the problem (what fails / where it fails).

## Severity (select one)
- [ ] blocker — project unusable / data loss
- [ ] critical — major functionality broken
- [ ] major — important feature broken or incorrect
- [ ] minor — small bug / cosmetic
- [ ] trivial — documentation / typo

## Questionnaire (please fill as many fields as you can)
- Project version: `uv run pip show <package>` / `pyproject.toml` version
- Python version: (e.g. `3.11.4`) — run `uv run python -V`
- OS / Distro: (e.g. macOS 13.4, Ubuntu 22.04)
- How installed: (e.g. `uv sync --group dev`, `uv sync --all-groups`, `uv run pip install .`, development `uv run pip install -e .`)
- Command(s) you ran (exact):
    ```bash
        # paste the exact command(s) you ran here
    ```
- Reproduction repository or gist: (link to a minimal repo showing the issue)
- Is the issue reproducible on latest main/branch? (yes / no / unknown)

## Steps to reproduce
Provide a numbered list of steps which reliably reproduce the bug. Prefer a minimal example.

1. 
2. 
3. 

## Expected behaviour
What you expected to happen.

## Actual behaviour
What actually happened (include full error message / exit code).

```text
# paste full traceback or terminal output here
```

## Temporary workarounds (optional)
Describe any workaround you found.

## Suggested fix (optional)
If you have a proposed fix, explain briefly or link a PR.

## Additional context / attachments (optional)
Screenshots, terminal recordings, or other artifacts that help debugging.
