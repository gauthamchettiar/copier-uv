"""Test the copier template can be copied without errors."""

import os
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def template_dir():
    """Return the path to the template directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary directory for the test project."""
    project_dir = tmp_path / "test-project"
    project_dir.mkdir()
    return project_dir


@pytest.fixture(scope="module")
def generated_hello_project(tmp_path_factory):
    """Generate a project with hello example and reuse it across tests."""
    template_dir = Path(__file__).parent.parent
    project_dir = tmp_path_factory.mktemp("projects") / "hello-project"
    
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
    
    # Initialize git repository
    git_init_result = subprocess.run(
        ["git", "init"],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    
    assert git_init_result.returncode == 0, f"Failed to init git:\n{git_init_result.stderr}"
    
    # Create and switch to a feature branch to avoid pre-commit branch protection
    git_branch_result = subprocess.run(
        ["git", "checkout", "-b", "feature/test"],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    
    assert git_branch_result.returncode == 0, f"Failed to create branch:\n{git_branch_result.stderr}"
    
    # Add all files and create initial commit for git-changelog
    subprocess.run(["git", "add", "."], cwd=project_dir, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "feat: initial project setup", "--no-verify"],
        cwd=project_dir,
        capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.com", "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.com"},
    )
    
    # Sync dependencies including all groups
    sync_result = subprocess.run(
        ["uv", "sync", "--all-groups"],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    
    assert sync_result.returncode == 0, f"Failed to sync dependencies:\n{sync_result.stderr}"
    
    return project_dir


@pytest.fixture(scope="module")
def generated_calculator_project(tmp_path_factory):
    """Generate a project with calculator example and reuse it across tests."""
    template_dir = Path(__file__).parent.parent
    project_dir = tmp_path_factory.mktemp("projects") / "calculator-project"
    
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
    
    assert result.returncode == 0, f"Failed to generate calculator project:\n{result.stderr}"
    
    # Initialize git repository
    git_init_result = subprocess.run(
        ["git", "init"],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    
    assert git_init_result.returncode == 0, f"Failed to init git:\n{git_init_result.stderr}"
    
    # Create and switch to a feature branch to avoid pre-commit branch protection
    git_branch_result = subprocess.run(
        ["git", "checkout", "-b", "feature/test"],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    
    assert git_branch_result.returncode == 0, f"Failed to create branch:\n{git_branch_result.stderr}"
    
    # Add all files and create initial commit for git-changelog
    subprocess.run(["git", "add", "."], cwd=project_dir, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "feat: initial project setup", "--no-verify"],
        cwd=project_dir,
        capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.com", "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.com"},
    )
    
    # Sync dependencies including all groups
    sync_result = subprocess.run(
        ["uv", "sync", "--all-groups"],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    
    assert sync_result.returncode == 0, f"Failed to sync dependencies:\n{sync_result.stderr}"
    
    return project_dir


def test_copier_copy_success(template_dir, temp_project):
    """Test that copier can copy the template without errors."""
    # Run copier with default values (non-interactive)
    result = subprocess.run(
        [
            "copier",
            "copy",
            "--defaults",
            "--trust",
            "--vcs-ref=HEAD",
            str(template_dir),
            str(temp_project),
        ],
        capture_output=True,
        text=True,
    )
    
    # Check that copier ran successfully
    assert result.returncode == 0, f"Copier failed with error:\n{result.stderr}"
    
    # Verify that key files were created
    assert (temp_project / "pyproject.toml").exists(), "pyproject.toml not created"
    assert (temp_project / "README.md").exists(), "README.md not created"
    assert (temp_project / ".copier-answers.yml").exists(), ".copier-answers.yml not created"
    

def test_copier_copy_with_custom_values(template_dir, temp_project):
    """Test that copier can copy the template with custom values."""
    # Run copier with custom data
    result = subprocess.run(
        [
            "copier",
            "copy",
            "--defaults",
            "--trust",
            "--vcs-ref=HEAD",
            "--data=project_name=My Test Project",
            "--data=project_slug=my_test_project",
            "--data=project_description=A test project",
            "--data=author_name=Test Author",
            "--data=author_email=test@example.com",
            "--data=min_python_version=3.10",
            "--data=example=hello",
            str(template_dir),
            str(temp_project),
        ],
        capture_output=True,
        text=True,
    )
    
    # Check that copier ran successfully
    assert result.returncode == 0, f"Copier failed with error:\n{result.stderr}"
    
    # Verify project structure
    assert (temp_project / "pyproject.toml").exists()
    assert (temp_project / "src" / "my_test_project").exists()
    assert (temp_project / "src" / "my_test_project" / "__init__.py").exists()
    assert (temp_project / "src" / "my_test_project" / "hello.py").exists()
    assert (temp_project / "tests" / "test_hello.py").exists()
    
    # Verify content in pyproject.toml
    pyproject_content = (temp_project / "pyproject.toml").read_text()
    assert "my-test-project" in pyproject_content or "my_test_project" in pyproject_content
    assert "Test Author" in pyproject_content
    assert "test@example.com" in pyproject_content


def test_copier_copy_calculator_example(generated_calculator_project):
    """Test that copier can copy the template with calculator example."""
    # Verify calculator-specific files exist
    project_slug = (generated_calculator_project / "src").iterdir().__next__().name
    assert (generated_calculator_project / "src" / project_slug / "calculator.py").exists()
    assert (generated_calculator_project / "tests" / "test_calculator.py").exists()
    assert (generated_calculator_project / "tests" / "conftest.py").exists()
    assert (generated_calculator_project / "tests" / "types.py").exists()


def test_generated_project_structure(template_dir, temp_project):
    """Test that the generated project has the expected structure."""
    # Run copier
    subprocess.run(
        [
            "copier",
            "copy",
            "--trust",
            "--defaults",
            "--vcs-ref=HEAD",
            str(template_dir),
            str(temp_project),
        ],
        capture_output=True,
        text=True,
    )
    
    # Check for expected directories
    assert (temp_project / "src").exists()
    assert (temp_project / "tests").exists()
    assert (temp_project / "docs").exists()
    
    # Check for expected files
    expected_files = [
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "zensical.toml",
        ".copier-answers.yml",
    ]
    
    for file in expected_files:
        assert (temp_project / file).exists(), f"{file} not created"


def test_poe_check_hello_example(generated_hello_project):
    """Test that poe check runs successfully on generated project with hello example."""
    # Run poe check in the generated project
    result = subprocess.run(
        ["uv", "run", "poe", "check"],
        cwd=generated_hello_project,
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, (
        f"poe check failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


def test_poe_check_calculator_example(generated_calculator_project):
    """Test that poe check runs successfully on generated project with calculator example."""
    # Run poe check in the generated project
    result = subprocess.run(
        ["uv", "run", "poe", "check"],
        cwd=generated_calculator_project,
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, (
        f"poe check failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


def test_poe_docs_hello_example(generated_hello_project):
    """Test that poe docs runs successfully on generated project with hello example."""
    # Run poe docs in the generated project
    result = subprocess.run(
        ["uv", "run", "poe", "docs"],
        cwd=generated_hello_project,
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, (
        f"poe docs failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    
    # Verify the docs site was built
    assert (generated_hello_project / "public").exists(), "Documentation site not created"
    assert (generated_hello_project / "public" / "index.html").exists(), "index.html not created"
    assert (generated_hello_project / "public" / "api" / "hello" / "index.html").exists(), "API reference page not created"


def test_poe_docs_calculator_example(generated_calculator_project):
    """Test that poe docs runs successfully on generated project with calculator example."""
    # Run poe docs in the generated project
    result = subprocess.run(
        ["uv", "run", "poe", "docs"],
        cwd=generated_calculator_project,
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, (
        f"poe docs failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    
    # Verify the docs site was built
    assert (generated_calculator_project / "public").exists(), "Documentation site not created"
    assert (generated_calculator_project / "public" / "index.html").exists(), "index.html not created"
    assert (generated_calculator_project / "public" / "api" / "calculator" / "index.html").exists(), "API reference page not created"

def test_poe_security_hello_example(generated_hello_project):
    """Test that poe security runs successfully on generated project with hello example."""
    # Run poe security in the generated project
    result = subprocess.run(
        ["uv", "run", "poe", "security"],
        cwd=generated_hello_project,
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, (
        f"poe security failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


def test_poe_pre_commit_hello_example(generated_hello_project):
    """Test that pre-commit runs successfully on generated project with hello example."""
    # Install pre-commit hooks
    install_result = subprocess.run(
        ["uv", "run", "pre-commit", "install"],
        cwd=generated_hello_project,
        capture_output=True,
        text=True,
    )

    assert install_result.returncode == 0, (
        f"pre-commit install failed:\nSTDOUT:\n{install_result.stdout}\nSTDERR:\n{install_result.stderr}"
    )

    # Run pre-commit on all files
    result = subprocess.run(
        ["uv", "run", "pre-commit", "run", "--all-files"],
        cwd=generated_hello_project,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"pre-commit run failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


def test_poe_pre_commit_calculator_example(generated_calculator_project):
    """Test that pre-commit runs successfully on generated project with calculator example."""
    # Install pre-commit hooks
    install_result = subprocess.run(
        ["uv", "run", "pre-commit", "install"],
        cwd=generated_calculator_project,
        capture_output=True,
        text=True,
    )

    assert install_result.returncode == 0, (
        f"pre-commit install failed:\nSTDOUT:\n{install_result.stdout}\nSTDERR:\n{install_result.stderr}"
    )

    # Run pre-commit on all files
    result = subprocess.run(
        ["uv", "run", "pre-commit", "run", "--all-files"],
        cwd=generated_calculator_project,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"pre-commit run failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


def test_poe_gen_hello_example(generated_hello_project):
    """Test that poe gen runs successfully on generated project with hello example."""
    # Run poe gen in the generated project
    result = subprocess.run(
        ["uv", "run", "poe", "gen"],
        cwd=generated_hello_project,
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, (
        f"poe gen failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    
    # Verify CHANGELOG.md was generated/updated
    assert (generated_hello_project / "CHANGELOG.md").exists(), "CHANGELOG.md not found"
    changelog_content = (generated_hello_project / "CHANGELOG.md").read_text()
    # git-changelog generates proper structure even with one commit
    assert "# Changelog" in changelog_content, "CHANGELOG.md missing title"
    assert "## Unreleased" in changelog_content, "CHANGELOG.md missing Unreleased section"
