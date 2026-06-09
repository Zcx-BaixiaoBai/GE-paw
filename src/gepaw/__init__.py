"""GE-paw 根包。

Top-level re-exports for the major subpackages so callers can do
``import gepaw; gepaw.providers`` without explicit submodule
imports.  Concrete heavy modules (providers, security, plugins,
app, etc.) are lazy via ``__getattr__`` where they might pull in
optional dependencies.
"""
from __future__ import annotations

from .__version__ import __version__


__all__ = ["__version__"]


_SUBMODULE_EXPORTS = (
    "agents",
    "app",
    "config",
    "constant",
    "exceptions",
    "plugins",
    "providers",
    "security",
    "token_usage",
    "utils",
    "wiki",
)


def __getattr__(name: str):  # type: ignore[no-untyped-def]
    if name in _SUBMODULE_EXPORTS:
        import importlib
        return importlib.import_module(f"gepaw.{name}")
    raise AttributeError(f"module 'gepaw' has no attribute {name!r}")


def __dir__() -> list:
    return sorted(list(globals().keys()) + list(_SUBMODULE_EXPORTS))