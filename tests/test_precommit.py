
import os
import subprocess
import pytest
import shutil

from tests.conftest import EXAMPLE_PROJECTS

@pytest.fixture(scope="module")
def temp_example_project_dirs_with_deps(temp_example_project_dirs):
    for project_name, project_dir in temp_example_project_dirs.items():
        print(f"\nSetting up dependencies in {project_name}: '{project_dir}'...")

        # Initialize git repository
        git_init_result = subprocess.run(
            ["git", "init"],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )
        
        assert git_init_result.returncode == 0, f"Failed to init git:\n{git_init_result.stderr}"

    yield temp_example_project_dirs

    # Clean up git directories for each project
    for project_name, project_dir in temp_example_project_dirs.items():
        print(f"\nCleaning up dependencies in {project_name}: '{project_dir}'...")
        
        git_dir = os.path.join(project_dir, ".git")
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir, ignore_errors=True)
        
        assert not os.path.exists(git_dir), f"Failed to remove .git directory in {project_name} project"

@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_precommit_run(example_project, temp_example_project_dirs_with_deps):
    """Test that pre-commit run command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]
    result = subprocess.run(
        ["uv", "run", "--with", "pre-commit", "pre-commit", "run", "--all-files"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Pre-commit run failed in {example_project} project:\n{result.stderr}"

