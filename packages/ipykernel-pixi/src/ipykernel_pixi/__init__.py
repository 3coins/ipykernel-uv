"""An IPython kernel that uses pixi for package and environment management."""

from .backend import PixiBackend

__version__ = "0.1.0"

__all__ = ["PixiBackend", "__version__"]
