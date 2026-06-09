from pathlib import Path
p = Path('src/aiohttp/__init__.py')
data = p.read_text()

old = '''class _Fallback:
    """A callable stub that yields a stub instance for any attribute access."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, name: str) -> "_Fallback":
        return _Fallback

    def __call__(self, *args: Any, **kwargs: Any) -> "_Fallback":
        return _Fallback(**kwargs)


def __getattr__(name: str) -> Any:
    """Lazy fallback for additional aiohttp symbols."""
    if name == "web":
        return _WebModule()
    return _Fallback


class _WebModule:
    """Stub aiohttp.web submodule providing common symbols."""

    def __getattr__(self, name: str) -> _Fallback:
        return _Fallback'''

new = '''class _Fallback:
    """A stub that supports any attribute access and calling."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, name: str) -> "_Fallback":
        return _Fallback()

    def __call__(self, *args: Any, **kwargs: Any) -> "_Fallback":
        return _Fallback(**kwargs)


def __getattr__(name: str) -> Any:
    """Lazy fallback for additional aiohttp symbols."""
    if name == "web":
        return _WebModule()
    return _Fallback()


class _WebModule:
    """Stub aiohttp.web submodule providing common symbols."""

    def __getattr__(self, name: str) -> _Fallback:
        return _Fallback()'''

print('found:', old in data)
data = data.replace(old, new)
p.write_text(data)
print('done')
