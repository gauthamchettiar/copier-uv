from pathlib import Path
import subprocess
import pytest

EXAMPLE_PROJECTS = ["hello", "calculator"]

@pytest.fixture(scope="session")
def template_dir():
    """Return the path to the template directory."""
    return Path(__file__).parent.parent

@pytest.fixture(scope="function")
def temp_project_dir(tmp_path_factory):
    """Create a temporary directory for the test project."""
    return tmp_path_factory.mktemp("test-project")

@pytest.fixture(scope="module")
def temp_hello_project_dir(template_dir, tmp_path_factory):
    """Create a temporary directory for the test project."""
    project_dir = tmp_path_factory.mktemp("test-hello-project")
    
    result = subprocess.run(
        [
            "copier",
            "copy",
            "--trust",
            "--defaults",
            "--vcs-ref=HEAD",
            "--data=example=hello",
            str(template_dir),
            str(project_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"Failed to generate hello project:\n{result.stderr}"
    
    return project_dir

@pytest.fixture(scope="module")
def temp_calc_project_dir(template_dir, tmp_path_factory):
    """Create a temporary directory for the test project."""
    project_dir = tmp_path_factory.mktemp("test-calc-project")

    result = subprocess.run(
        [
            "copier",
            "copy",
            "--trust",
            "--defaults",
            "--vcs-ref=HEAD",
            "--data=example=calculator",
            str(template_dir),
            str(project_dir),
        ],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, f"Failed to generate calc project:\n{result.stderr}"

    return project_dir

@pytest.fixture(scope="module")
def temp_example_project_dirs(temp_hello_project_dir, temp_calc_project_dir):
    example_project_dirs = {
        "hello": temp_hello_project_dir,
        "calculator": temp_calc_project_dir,
    }
    
    return example_project_dirs

@pytest.fixture(scope="module")
def expected_common_files():
    return set([
        ".pre-commit-config.yaml",
        ".copier-answers.yml",
        ".secrets.baseline",
        ".gitignore",
        ".python-version",
        ".github/dependabot.yml",
        ".github/workflows/ci.yml",
        ".github/workflows/docs.yml",
        ".github/workflows/release.yml",
        ".github/ISSUE_TEMPLATE/bug-report---.md",
        ".github/ISSUE_TEMPLATE/feature-request---.md",
        "CHANGELOG.md",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "LICENSE",
        "pyproject.toml",
        "README.md",
        "zensical.toml",
        "docs/changelog.md",
        "docs/code_of_conduct.md",
        "docs/contributing.md",
        "docs/index.md",
        "docs/license.md",
        "images/logo.png",
        "tests/__init__.py",
    ])

@pytest.fixture(scope="module")
def expected_hello_example_project_files(expected_common_files, temp_hello_project_dir):
    hello_project_stub = temp_hello_project_dir.name.replace("-", "_")
    return expected_common_files | set([
        f"src/{hello_project_stub}/__init__.py",
        f"src/{hello_project_stub}/py.typed",
        f"src/{hello_project_stub}/hello.py",
        "docs/api/hello.md",
        "tests/test_hello.py",
    ])

@pytest.fixture(scope="module")
def expected_calc_example_project_files(expected_common_files, temp_calc_project_dir):
    calc_project_stub = temp_calc_project_dir.name.replace("-", "_")
    return expected_common_files | set([
        f"src/{calc_project_stub}/__init__.py",
        f"src/{calc_project_stub}/py.typed",
        f"src/{calc_project_stub}/calculator.py",
        "docs/api/calculator.md",
        "tests/test_calculator.py",
        "tests/conftest.py",
        "tests/types.py",
    ])

@pytest.fixture(scope="module")
def expected_example_project_files(expected_hello_example_project_files, expected_calc_example_project_files):
    return {
        "hello": expected_hello_example_project_files,
        "calculator": expected_calc_example_project_files,
    }

@pytest.fixture(scope="module")
def expected_poe_tasks():
    return set([
        "lint",
        "lint-fix",
        "format",
        "format-check",
        "type-check",
        "security-bandit",
        "security-audit",
        "docs-serve",
        "docs-build",
        "docs-clean",
        "test-unit",
        "test-integration",
        "test",
        "test-cov-check",
        "test-cov-gen",
        "test-py313",
        "clean",
        "check",
        "fix",
        "test-pyall",
        "security",
        "docs",
    ])