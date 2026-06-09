from pathlib import Path
p = Path("src/gepaw/app/channels/base.py")
data = p.read_bytes()
old = b"""class IncomingMessage:\r\n    \"\"\"Stub `IncomingMessage` channel payload.\"\"\"\r\n\r\n    def __init__(self, *args, **kwargs) -> None:\r\n        for k, v in kwargs.items():\r\n            setattr(self, k, v)\r\n"""
new = b"""class IncomingMessage:\r\n    \"\"\"Stub `IncomingMessage` channel payload.\"\"\"\r\n\r\n    def __init__(self, *args, **kwargs) -> None:\r\n        self.raw: Optional[Dict[str, Any]] = None\r\n        for k, v in kwargs.items():\r\n            setattr(self, k, v)\r\n        if not hasattr(self, \"raw\") or self.raw is None:\r\n            self.raw = {}\r\n"""
print("found:", old in data)
data = data.replace(old, new)
p.write_bytes(data)
print("done")
