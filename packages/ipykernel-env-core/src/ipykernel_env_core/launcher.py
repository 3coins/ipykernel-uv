"""Backend-agnostic kernel launch flow.

The sequence is identical for every backend:

1. Confirm the manager is installed.
2. Find the nearest project manifest, or create one.
3. Clear inherited virtual-env variables so the manager owns the environment.
4. Ensure ``ipykernel`` is a declared dependency.
5. Exec into ``ipykernel_launcher`` inside the managed environment.

The per-manager differences live entirely in the :class:`Backend`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .backend import Backend

# Variables from the launching (JupyterLab) environment that would otherwise
# leak into and confuse the manager-owned environment.
_ENV_VARS_TO_CLEAR = ("VIRTUAL_ENV", "CONDA_PREFIX", "CONDA_DEFAULT_ENV")


def launch_kernel(backend: Backend, args: list[str]) -> None:
    """Run the launch flow for ``backend`` and exec into the kernel."""
    try:
        backend.check_available()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    cwd = Path.cwd()
    manifest = backend.find_manifest(cwd)
    if manifest is None:
        print(
            f"No project manifest found, creating one in {cwd} "
            f"using {backend.display}",
            file=sys.stderr,
        )
        manifest = backend.init_project(cwd)

    for var in _ENV_VARS_TO_CLEAR:
        os.environ.pop(var, None)

    backend.ensure_ipykernel(manifest)
    backend.exec_kernel(manifest, args)
