"""Find the nearest uv project and exec into ipykernel via uv run."""

import os
import shutil
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
        print("error: no pyproject.toml found in any parent directory", file=sys.stderr)
        sys.exit(1)

    project_dir = str(pyproject.parent)

    cmd = [
        uv,
        "run",
        "--project",
        project_dir,
        "--with",
        "ipykernel",
        "python",
        "-m",
        "ipykernel_launcher",
        *args,
    ]

    os.execvp(cmd[0], cmd)
