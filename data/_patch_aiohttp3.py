from pathlib import Path
p = Path('src/aiohttp/__init__.py')
data = p.read_text()

old = '''class _Fallback:
    """A stub that supports any attribute access and calling."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, name: str) -> "_Fallback":
        return _Fallback()

    def __call__(self, *args: Any, **kwargs: Any) -> "_Fallback":
        return _Fallback(**kwargs)'''

new = '''class _Fallback:
    """A stub that supports any attribute access, calling, and awaiting."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, name: str) -> "_Fallback":
        return _Fallback()

    def __call__(self, *args: Any, **kwargs: Any) -> "_Fallback":
        return _Fallback(**kwargs)

    def __await__(self):
        async def _coro():
            return self
        return _coro().__await__()'''

print('found:', old in data)
data = data.replace(old, new)
p.write_text(data)
print('done')
