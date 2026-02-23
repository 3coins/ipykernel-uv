"""Install the ipykernel-uv kernel spec into Jupyter."""

import argparse
import json
import os
import sys
import tempfile


def install(
    name: str = "python3-uv",
    display_name: str = "Python (uv)",
    user: bool = False,
    prefix: str | None = None,
) -> None:
    """Create and install the kernel spec."""
    from jupyter_client.kernelspec import KernelSpecManager

    kernel_json = {
        "argv": [sys.executable, "-m", "ipykernel_uv", "-f", "{connection_file}"],
        "display_name": display_name,
        "language": "python",
        "metadata": {"debugger": True},
    }

    with tempfile.TemporaryDirectory() as td:
        kernel_dir = os.path.join(td, name)
        os.makedirs(kernel_dir)
        with open(os.path.join(kernel_dir, "kernel.json"), "w") as f:
            json.dump(kernel_json, f, indent=1)

        ksm = KernelSpecManager()
        ksm.install_kernel_spec(kernel_dir, kernel_name=name, user=user, prefix=prefix)

    print(f"Installed kernel spec: {name}")


def install_main(argv: list[str]) -> None:
    """Parse CLI args and install the kernel spec."""
    parser = argparse.ArgumentParser(
        description="Install the ipykernel-uv kernel spec"
    )
    parser.add_argument(
        "--name", default="python3-uv", help="kernel name (default: python3-uv)"
    )
    parser.add_argument(
        "--display-name",
        default="Python (uv)",
        help="display name (default: Python (uv))",
    )
    parser.add_argument(
        "--user", action="store_true", help="install for the current user"
    )
    parser.add_argument("--prefix", help="install under a specific prefix")
    parser.add_argument(
        "--sys-prefix",
        action="store_true",
        help="install into sys.prefix (e.g. a virtualenv)",
    )
    args = parser.parse_args(argv)

    prefix = args.prefix
    if args.sys_prefix:
        prefix = sys.prefix

    install(
        name=args.name,
        display_name=args.display_name,
        user=args.user,
        prefix=prefix,
    )
