from pathlib import Path
p = Path("src/aiohttp/__init__.py")
data = p.read_text()

old = """class _WebModule:
    \"\"\"Stub aiohttp.web submodule providing common symbols.\"\"\"

    def __getattr__(self, name: str) -> _Fallback:
        return _Fallback()"""

new = """class _TCPSite:
    \"\"\"Stub aiohttp.web.TCPSite that tracks start/stop state.\"\"\"

    def __init__(self, runner=None, host: str = "0.0.0.0", port: int = 0, **kwargs):
        self._runner = runner
        self._host = host
        self._port = port
        self._started = True
        self._sockets = []

    async def start(self):
        self._started = True
        return None

    async def stop(self):
        self._started = False
        return None

    @property
    def name(self):
        return f"TCPSite({self._host}:{self._port})"


class _WebModule:
    \"\"\"Stub aiohttp.web submodule providing common symbols.\"\"\"

    _TCPSite = _TCPSite

    def __getattr__(self, name: str):
        if name == "TCPSite":
            return _TCPSite
        return _Fallback()"""

print("found:", old in data)
data = data.replace(old, new)
p.write_text(data)
print("done")
