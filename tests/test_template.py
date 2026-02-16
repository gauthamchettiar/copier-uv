
import pytest

from tests.conftest import EXAMPLE_PROJECTS

@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_copier_copy_success_using_default_values(example_project, temp_example_project_dirs):
    """Test that the copier copy command works successfully."""
    project_dir = temp_example_project_dirs[example_project]

    assert project_dir.exists(), f"{example_project} project directory was not created."

@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_copied_files_existence_using_default_values(example_project, temp_example_project_dirs, expected_example_project_files):
    """Test that the expected files are created in the generated projects."""
    project_dir = temp_example_project_dirs[example_project]
    expected_files = expected_example_project_files[example_project]
    actual_files = set(str(file.relative_to(project_dir)) for file in project_dir.rglob("*") if file.is_file())
    
    assert actual_files == expected_files, f"{example_project} project files do not match expected files. Missing Files: {expected_files - actual_files}, Unexpected Files: {actual_files - expected_files}"