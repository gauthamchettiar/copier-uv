import subprocess

import pytest

from tests.conftest import EXAMPLE_PROJECTS

@pytest.fixture(scope="module")
def temp_example_project_dirs_with_deps(temp_example_project_dirs):
    for project_name, project_dir in temp_example_project_dirs.items():
        result = subprocess.run(
            ["uv", "sync", "--dev"],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Failed to install dependencies in {project_name} project:\n{result.stderr}"

    yield temp_example_project_dirs

    for project_name, project_dir in temp_example_project_dirs.items():
        print(f"\nCleaning up dependencies in {project_name} project...")
        result = subprocess.run(
            ["uv", "sync", "--no-dev"],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Failed to clean dependencies in {project_name} project:\n{result.stderr}"


def test_poe_command_help(temp_example_project_dirs_with_deps, expected_poe_tasks):
    """Test that poe --help command works in the generated projects."""
    result = subprocess.run(
        ["uv", "run", "poe", "--help"],
        cwd=temp_example_project_dirs_with_deps["hello"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe --help failed in project:\n{result.stderr}"

    # Parse the stdout to extract commands
    lines = result.stdout.split('\n')
    actual_poe_tasks = set()
    in_task_section = False
    for line in lines:
        if 'Configured tasks:' in line:
            in_task_section = True
            continue

        if in_task_section:
            if line.startswith('    '):
                continue  # Skip args that are not commands
            else:
                stripped_line = line.strip()
                if stripped_line:
                    command = stripped_line.split()[0]
                    actual_poe_tasks.add(command)

    assert set(actual_poe_tasks) == set(expected_poe_tasks), (
        f"Expected commands do not match actual commands. Missing commands: {set(expected_poe_tasks) - set(actual_poe_tasks)}, "
        f"Unexpected commands: {set(actual_poe_tasks) - set(expected_poe_tasks)}"
    )


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_lint(example_project, temp_example_project_dirs_with_deps):
    """Test that poe lint command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "lint"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe lint failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => ruff check src tests" in line for line in result.stderr.splitlines()), (
        f"Poe lint did not run ruff check in {example_project} project:\n{result.stderr}"
    )

    result = subprocess.run(
        ["uv", "run", "poe", "lint", "src"],
        cwd=project_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Poe lint src failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => ruff check src" in line for line in result.stderr.splitlines()), (
        f"Poe lint src did not run ruff check on src in {example_project} project:\n{result.stderr}"
    )


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_lint_fix(example_project, temp_example_project_dirs_with_deps):
    """Test that poe lint --fix command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "lint-fix"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe lint --fix failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => ruff check src tests --fix" in line for line in result.stderr.splitlines()), (
        f"Poe lint --fix did not run ruff fix in {example_project} project:\n{result.stderr}"
    )

    result = subprocess.run(
        ["uv", "run", "poe", "lint-fix", "src"],
        cwd=project_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Poe lint --fix src failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => ruff check src --fix" in line for line in result.stderr.splitlines()), (
        f"Poe lint --fix src did not run ruff fix on src in {example_project} project:\n{result.stderr}"
    )


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_format(example_project, temp_example_project_dirs_with_deps):
    """Test that poe format command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "format"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe format failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => ruff format src tests" in line for line in result.stderr.splitlines()), (
        f"Poe format did not run ruff format in {example_project} project:\n{result.stderr}"
    )

    result = subprocess.run(
        ["uv", "run", "poe", "format", "src"],
        cwd=project_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Poe format src failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => ruff format src" in line for line in result.stderr.splitlines()), (
        f"Poe format src did not run ruff format on src in {example_project} project:\n{result.stderr}"
    )


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_format_check(example_project, temp_example_project_dirs_with_deps):
    """Test that poe format --check command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "format-check"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe format --check failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => ruff format src tests --check" in line for line in result.stderr.splitlines()), (
        f"Poe format --check did not run ruff format --check in {example_project} project:\n{result.stderr}"
    )

    result = subprocess.run(
        ["uv", "run", "poe", "format-check", "src"],
        cwd=project_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Poe format --check src failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => ruff format src --check" in line for line in result.stderr.splitlines()), (
        f"Poe format --check src did not run ruff format --check on src in {example_project} project:\n{result.stderr}"
    )


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_type_check(example_project, temp_example_project_dirs_with_deps):
    """Test that poe type-check command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "type-check"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe type-check failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => pyright src tests" in line for line in result.stderr.splitlines()), (
        f"Poe type-check did not run pyright in {example_project} project:\n{result.stderr}"
    )

    result = subprocess.run(
        ["uv", "run", "poe", "type-check", "src"],
        cwd=project_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Poe type-check src failed in {example_project} project:\n{result.stderr}"
    assert any("Poe => pyright src" in line for line in result.stderr.splitlines()), (
        f"Poe type-check src did not run pyright on src in {example_project} project:\n{result.stderr}"
    )


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_security_bandit(example_project, temp_example_project_dirs_with_deps):
    """Test that poe security-bandit command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "security-bandit"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe security-bandit failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_security_audit(example_project, temp_example_project_dirs_with_deps):
    """Test that poe security-audit command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "security-audit"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe security-audit failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_docs_build_clean(example_project, temp_example_project_dirs_with_deps):
    """Test that poe docs-build command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "docs-build"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe docs-build failed in {example_project} project:\n{result.stderr}"
    assert (project_path / "public").exists(), f"Docs build directory was not created in {example_project} project"

    result = subprocess.run(
        ["uv", "run", "poe", "docs-clean"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe docs-clean failed in {example_project} project:\n{result.stderr}"
    assert not (project_path / "public").exists(), f"Docs build directory was not removed in {example_project} project"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_test_unit(example_project, temp_example_project_dirs_with_deps):
    """Test that poe test-unit command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "test-unit"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe test-unit failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_test_integration(example_project, temp_example_project_dirs_with_deps):
    """Test that poe test-integration command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "test-integration"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    if example_project == "hello":
        # hello project has no integration tests, so it should return 5 (no tests collected)
        assert result.returncode == 5, f"Poe test-integration failed in {example_project} project:\n{result.stdout}"
    else:
        assert result.returncode == 0, f"Poe test-integration failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_test(example_project, temp_example_project_dirs_with_deps):
    """Test that poe test command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "test"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe test failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_test_cov_check(example_project, temp_example_project_dirs_with_deps):
    """Test that poe test-cov-check command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "test-cov-check"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe test-cov-check failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_test_cov_gen(example_project, temp_example_project_dirs_with_deps):
    """Test that poe test-cov-gen command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "test-cov-gen"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe test-cov-gen failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_test_py(example_project, temp_example_project_dirs_with_deps):
    """Test that poe test-py{version} command works in the generated projects."""
    latest_version_supported =  "313" # Update this to the latest Python version supported by the template
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", f"test-py{latest_version_supported}"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe test-py{latest_version_supported} failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_test_pyall(example_project, temp_example_project_dirs_with_deps):
    """Test that poe test-pyall command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "test-pyall"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe test-pyall failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_clean(example_project, temp_example_project_dirs_with_deps):
    """Test that poe clean command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "clean"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe clean failed in {example_project} project:\n{result.stderr}"
    
    files_cleaned = ['.pytest_cache', '__pycache__', 'build', 'dist', 'htmlcov', '.mypy_cache', '.ruff_cache', 'public']
    for file in files_cleaned:
        assert not (project_path / file).exists(), f"{file} was not removed in {example_project} project"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_check(example_project, temp_example_project_dirs_with_deps):
    """Test that poe check command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "check"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe check failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_fix(example_project, temp_example_project_dirs_with_deps):
    """Test that poe fix command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "fix"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe fix failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_security(example_project, temp_example_project_dirs_with_deps):
    """Test that poe security command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "security"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe security failed in {example_project} project:\n{result.stderr}"


@pytest.mark.parametrize("example_project", EXAMPLE_PROJECTS)
def test_poe_docs(example_project, temp_example_project_dirs_with_deps):
    """Test that poe docs command works in the generated projects."""
    project_path = temp_example_project_dirs_with_deps[example_project]

    result = subprocess.run(
        ["uv", "run", "poe", "docs"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Poe docs failed in {example_project} project:\n{result.stderr}"
