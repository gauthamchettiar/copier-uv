# copier-uv 

A modern Copier template for Python projects.

## Features

### Project Management
- **UV-based dependency management** - Fast, modern Python package and project management
- **Ruff** for fast linting and formatting with extensive rule sets including:
  - pycodestyle, Pyflakes, isort, pep8-naming, pydocstyle
  - pyupgrade, flake8-bugbear, flake8-bandit security checks
  - flake8-comprehensions, flake8-pytest-style, and many more
- **Pyright** for strict type checking with full configuration
  - **Bandit** for security vulnerability scanning
- **pip-audit** for dependency vulnerability checks
- **detect-secrets** pre-commit hook with baseline configuration (.secrets.baseline)
- **Pre-commit hooks** for automated quality checks including:
  - `trailing-whitespace` - Remove trailing whitespace
  - `end-of-file-fixer` - Ensure files end with newline
  - `check-merge-conflict` - Detect merge conflict markers
  - `check-yaml` - Validate YAML file syntax
  - `check-toml` - Validate TOML file syntax
  - `check-added-large-files` - Prevent large files (>1MB) from being committed
  - `no-commit-to-branch` - Prevent direct commits to main/master
  - `detect-secrets` - Scan for accidentally committed secrets
  - `poe pre-commit` - Run format + lint-fix on pre-commit stage
  - (push only) `poe check` - Run full test suite + type checking + linting on pre-push stage

### Testing
- **Pytest** configuration with coverage support
- **pytest-cov** for code coverage reporting (80% minimum threshold)
- **Multi-version testing** support across Python 3.10, 3.11, 3.12, 3.13
- **Pytest markers support** Separate unit and integration test markers

### CI/CD
- **GitHub Actions** workflows for automated testing and checks
- **Matrix testing** across multiple Python versions
- **Pre-commit** and **pre-push** hooks for local validation
- **Dependabot** configuration for automated dependency updates
- **Renovate** support (optional) for advanced dependency management

### Documentation
- **MkDocs** with Material theme for beautiful documentation
- **mkdocstrings** for automatic API documentation from docstrings
- Pre-configured pages: Home, Changelog, Contributing, Code of Conduct, License, Credits, Coverage
- Auto-generated coverage reports in documentation

### Task Automation
- **Poe the Poet** task runner with pre-configured tasks:
  - Linting (`lint`, `lint-fix`)
  - Formatting (`format`, `format-check`)
  - Type checking (`type-check`)
  - Security checks (`security-bandit`, `security-audit`)
  - Testing (`test-unit`, `test-integration`, `test-cov-check`)
  - Documentation (`docs-serve`, `docs-build`)
  - Changelog generation (`gen-changelog`)
  - Aggregate tasks (`check`, `fix`, `security`, `ci`)

### Project Files
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

## Usage

To create a new project from this template, run:

```bash
copier copy gh:gauthamchettiar/copier-uv <destination-folder>
```

or if you have a local copy of the template:

```bash
copier copy /path/to/copier-uv <destination-folder>
```

## Development

### Running Tests

This template includes tests to verify that the copier template works correctly. To run the tests:

```bash
uv sync          # Install dependencies (first time only)
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
