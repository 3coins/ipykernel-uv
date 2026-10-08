# ipykernel-env

Jupyter kernels that automatically manage a project's environment for you. Select the
kernel, and it finds (or creates) the project manifest, makes sure `ipykernel` is
declared, and launches IPython inside the managed environment — no manual virtual
environment juggling.

This is a monorepo with a shared core and one package per environment manager:

| Package | Manager | Kernel | Dist |
|---|---|---|---|
| [`packages/ipykernel-env-core`](packages/ipykernel-env-core) | — | — | `ipykernel-env-core` |
| [`packages/ipykernel-uv`](packages/ipykernel-uv) | [uv](https://docs.astral.sh/uv/) | Python (uv) | `ipykernel-uv` |
| [`packages/ipykernel-pixi`](packages/ipykernel-pixi) | [pixi](https://pixi.prefix.dev/) | Python (pixi) | `ipykernel-pixi` |

Install whichever backend you want — each pulls in `ipykernel-env-core`:

```bash
pip install ipykernel-uv      # Python (uv) kernel
pip install ipykernel-pixi    # Python (pixi) kernel
python -m ipykernel_uv install --user
python -m ipykernel_pixi install --user
```

See each package's README for details.

## Architecture

`ipykernel-env-core` defines a small `Backend` protocol and the backend-agnostic
launch/install flow:

```
find manifest (or init) -> clear inherited venv vars -> ensure ipykernel -> exec kernel
```

Each backend supplies the manager-specific pieces (manifest discovery, `init`, `add`,
`run`). The uv and pixi backends mirror each other:

| Step | uv | pixi |
|---|---|---|
| Manifest | `pyproject.toml` | `pixi.toml` or `pyproject.toml` with `[tool.pixi]` |
| Init if missing | `uv init --bare` | `pixi init --format pyproject` |
| Ensure ipykernel | `uv add ipykernel` | `pixi add ipykernel` |
| Launch | `uv run --project <dir> python -m ipykernel_launcher` | `pixi run --manifest-path <manifest> python -m ipykernel_launcher` |
| In-notebook add | `!uv add <pkg>` | `!pixi add <pkg>` |

Adding another manager is a new package implementing `Backend` — no change to the core
flow.

## Development

This repo is a [uv workspace](https://docs.astral.sh/uv/concepts/workspaces/).

```bash
# Clone
git clone https://github.com/jupyter-ai-contrib/ipykernel-env.git
cd ipykernel-env

# Sync all workspace packages into one dev environment
uv sync

# Install a kernel spec locally
uv run python -m ipykernel_uv install --sys-prefix
uv run python -m ipykernel_pixi install --sys-prefix
```

## License

BSD-3-Clause
