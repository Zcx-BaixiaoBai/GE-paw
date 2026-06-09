from pathlib import Path
p = Path("src/gepaw/app/channels/manager.py")
data = p.read_bytes()
old = b"import asyncio\r\nimport logging"
new = b"import asyncio\r\nimport logging\r\nimport threading"
print("found:", old in data)
data = data.replace(old, new)
p.write_bytes(data)
print("done")
