# ipykernel-uv

A Jupyter kernel that uses [uv](https://docs.astral.sh/uv/) to automatically manage
Python environments for your projects. When you select this kernel, it finds the nearest
`pyproject.toml`, syncs the project's dependencies with `uv`, and launches IPython inside
that environment — no manual virtual environment management required.

## How it works

1. You select the **Python (uv)** kernel in JupyterLab
2. The kernel finds the nearest `pyproject.toml` by walking up from the notebook's directory
3. If it can't find one, it creates ones in the notebook's directory
3. If `ipykernel` is not already in the project's dependencies, it adds it via `uv add`
4. It runs `uv run --project <dir> python -m ipykernel_launcher`
5. uv syncs the project's environment and starts IPython inside it

This means your notebook automatically has access to all the dependencies declared in your
project's `pyproject.toml`. The `ipykernel` package is added to your project's dependencies
automatically if not already present.

## Requirements

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) installed and available on PATH

## Installation

Install the package:

```bash
pip install ipykernel-uv
```

Or with uv:

```bash
uv pip install ipykernel-uv
```

Then register the kernel spec. Choose one of the following options:

```bash
# Install for the current user
python -m ipykernel_uv install --user

# Install into the current virtual environment
python -m ipykernel_uv install --sys-prefix

# Install into a specific prefix
python -m ipykernel_uv install --prefix /path/to/prefix
```

## Usage

1. Setup: `pyproject.toml` 
   - Make sure your project/directory has a `pyproject.toml` with its dependencies listed.
   - Or, if it can't find a nearby `pyproject.toml` one will be created.
2. Open JupyterLab and create or open a notebook in your project directory
3. Select the **Python (uv)** kernel from the kernel picker
4. Your notebook now runs inside your project's uv-managed environment
5. You can add new package using `!uv add <project>` inside a notebook cell.

## Install options

| Flag | Description |
|------|-------------|
| `--name` | Kernel name (default: `python3-uv`) |
| `--display-name` | Display name in Jupyter (default: `Python (uv)`) |
| `--user` | Install for the current user |
| `--sys-prefix` | Install into `sys.prefix` (e.g. the active virtual environment) |
| `--prefix` | Install into a specific prefix directory |

## Development

```bash
# Clone the repo
git clone https://github.com/jupyter-ai-contrib/ipykernel-uv.git
cd ipykernel-uv

# Sync the development environment
uv sync

# Install the kernel spec locally
uv run python -m ipykernel_uv install --sys-prefix
```

## License

BSD-3-Clause
