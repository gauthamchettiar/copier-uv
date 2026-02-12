# copier-uv 

[![CI](https://github.com/gauthamchettiar/copier-uv/actions/workflows/ci.yml/badge.svg)](https://github.com/gauthamchettiar/copier-uv/actions/workflows/ci.yml)

A modern Copier template for Python projects.

## Features
- Project managed with [uv](https://docs.astral.sh/uv/), with pre-configured [pyproject.toml](./project/pyproject.toml.jinja)
- [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, wih extensive rulesets.
- [Pyright](https://pypi.org/project/pyright/) for strict type checking.
- [pytest](https://docs.pytest.org/en/stable/) with multi-version testing support and coverage reporting.
- [Bandit](https://pypi.org/project/bandit/) and [pip-audit](https://pypi.org/project/pip-audit/) for security vulnerability.
- [pre-commit](https://pre-commit.com/) hooks for automated quality fixes and checks.
- [detect-secrets](https://github.com/Yelp/detect-secrets?tab=readme-ov-file) pre-commit hook for scanning committed secrets.
- [GitHub Actions](https://docs.github.com/en/actions) workflows for CI/CD automation.
- [Dependabot](https://github.com/dependabot) configuration for automated dependency updates.
- [Zensical](https://zensical.org/docs) for documentation, built on [MkDocs](https://www.mkdocs.org/) with [Material theme](https://squidfunk.github.io/mkdocs-material/), including auto-generated API docs with [mkdocstrings](https://mkdocstrings.github.io/).
- [Poe the Poet](https://poethepoet.natn.io/) for task automation.

### Included Files
- **README** with project information
- **LICENSE** (MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, or MPL-2.0)
- **CHANGELOG** with git-changelog integration
- **CONTRIBUTING** guide with development instructions
- **CODE_OF_CONDUCT** for community guidelines
- **.gitignore** pre-configured for Python projects
- Example modules (hello or calculator) to get started

### Multiple Starter Modules
You can choose between two example modules to include in your project:
- Example module: `hello` - A simple "Hello, World!" module (for a barebones project setup)
- Example module: `calculator` - A basic calculator module with arithmetic operations (has more tests examples, good for learning)

## Pre-requisites
- [Git](https://git-scm.com/)
- [Python 3.10+](https://www.python.org/downloads/)
- [Copier](https://copier.readthedocs.io/en/stable/#installation)
  - Install with UV:
      ```bash
      uv tool install copier --with copier-templates-extensions
      ```
  - Install with pipx:
      ```bash
      pipx install copier 
      pipx inject copier copier-templates-extensions
      ```

## Usage
To create a new project from this template, run:

```bash
copier copy gh:gauthamchettiar/copier-uv <destination-folder>
```

## Development

This template includes tests to verify that the copier template works correctly. To run the tests:

```bash
uv sync --dev    # Install dependencies (first time only)
uv run pytest    # Run tests
```

## Questions

When you run the copy command, you'll be asked the following questions:

1. **What is your project name?**
   - Default: The destination folder name
   - This will be used as the project's display name

2. **What is the Python package name (slug)?**
   - Default: Auto-generated from project name (lowercase, underscores instead of hyphens/spaces)
   - This will be the importable Python package name

3. **Project description**
   - Default: "A short description of the project."
   - A brief description of what your project does

4. **Author name**
   - Default: Detected from git config or "Your Name"
   - The name of the project author/maintainer

5. **Author email**
   - Default: Detected from git config or "your.name@example.com"
   - Contact email for the project author

6. **Author Repository username**
   - Default: Author name in lowercase without spaces
   - Your username on the repository platform (e.g., GitHub username)

7. **Your repository provider**
   - Default: `github.com`
   - Choices: `github.com`
   - The platform where your repository will be hosted

8. **Your repository namespace**
   - Default: Same as author username
   - The namespace/organization for your repository

9. **Your repository name**
   - Default: Slugified version of project_slug
   - The name of your repository

10. **Minimum Python version**
    - Default: `3.13`
    - Choices: `3.10`, `3.11`, `3.12`, `3.13`
    - The minimum Python version required for your project

11. **Choose a license**
    - Default: `MIT`
    - Choices: `MIT`, `Apache-2.0`, `BSD-3-Clause`, `GPL-3.0`, `MPL-2.0`
    - The open source license for your project

12. **Copyright year**
    - Default: Current year (2026)
    - The year for copyright notices

13. **Choose an example module**
    - Default: `hello`
    - Choices: `hello`, `calculator`
    - An example module to include in your project
