"""An IPython kernel that uses uv for package and environment management."""

from .backend import UvBackend

__version__ = "0.1.0"

__all__ = ["UvBackend", "__version__"]
