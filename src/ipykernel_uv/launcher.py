"""Find the nearest uv project and exec into ipykernel via uv run."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def find_pyproject_toml() -> Path | None:
    """Walk up from CWD to filesystem root looking for pyproject.toml."""
    current = Path.cwd().resolve()
    while True:
        candidate = current / "pyproject.toml"
        if candidate.is_file():
            return candidate
        parent = current.parent
        if parent == current:
            return None
        current = parent


def launch_kernel(args: list[str]) -> None:
    """Exec into uv run ... ipykernel_launcher with the given args."""
    uv = shutil.which("uv")
    if uv is None:
        print("error: uv not found on PATH", file=sys.stderr)
        print(
            "Install uv: https://docs.astral.sh/uv/getting-started/installation/",
            file=sys.stderr,
        )
        sys.exit(1)

    pyproject = find_pyproject_toml()
    if pyproject is None:
        cwd = Path.cwd()
        print(f"No pyproject.toml found, creating one in {cwd}", file=sys.stderr)
        subprocess.run([uv, "init", ".", "--bare"], check=True)
        pyproject = cwd / "pyproject.toml"

    project_dir = str(pyproject.parent)

    # Clear environment variables from the parent (JupyterLab) environment
    # so uv cleanly manages its own project environment.
    for var in ("VIRTUAL_ENV", "CONDA_PREFIX", "CONDA_DEFAULT_ENV"):
        os.environ.pop(var, None)

    # Ensure ipykernel is declared as a dependency in the project
    if not _has_ipykernel_dependency(pyproject):
        subprocess.run(
            [uv, "add", "--project", project_dir, "ipykernel"], check=True
        )

    cmd = [
        uv,
        "run",
        "--project",
        project_dir,
        "python",
        "-m",
        "ipykernel_launcher",
        *args,
    ]

    os.execvp(cmd[0], cmd)


def _has_ipykernel_dependency(pyproject: Path) -> bool:
    """Check if ipykernel is already listed in the project's dependencies."""
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib

    with open(pyproject, "rb") as f:
        data = tomllib.load(f)

    deps = data.get("project", {}).get("dependencies", [])
    return any(
        re.split(r"[><=!\[;~\s]", dep.strip())[0] == "ipykernel" for dep in deps
    )
