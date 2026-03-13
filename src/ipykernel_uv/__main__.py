"""Entry point for `python -m ipykernel_uv`."""

import sys


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        from .install import install_main

        install_main(sys.argv[2:])
    else:
        from .launcher import launch_kernel

        launch_kernel(sys.argv[1:])


if __name__ == "__main__":
    main()
