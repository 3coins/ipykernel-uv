# ipykernel-env-core

Shared core for environment-managed IPython kernels. Provides the `Backend`
abstraction and the launch/install plumbing used by the backend packages
([`ipykernel-uv`](../ipykernel-uv), [`ipykernel-pixi`](../ipykernel-pixi)).

You usually don't install this directly — install a backend package, which
depends on this one. Implement `Backend` to add a new environment manager.

## The `Backend` protocol

```python
class Backend(Protocol):
    name: str
    display: str
    def check_available(self) -> str: ...
    def find_manifest(self, start: Path) -> Path | None: ...
    def init_project(self, directory: Path) -> Path: ...
    def ensure_ipykernel(self, manifest: Path) -> None: ...
    def exec_kernel(self, manifest: Path, args: list[str]) -> NoReturn: ...
```

A backend package wires it up in its `__main__`:

```python
from ipykernel_env_core import launch_kernel, install_main
from .backend import MyBackend

backend = MyBackend()
# install path: install_main(argv, module="ipykernel_mine", ...)
# launch path:  launch_kernel(backend, args)
```

## License

BSD-3-Clause
