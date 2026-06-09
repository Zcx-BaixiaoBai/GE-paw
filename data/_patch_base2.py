from pathlib import Path
p = Path("src/gepaw/app/channels/base.py")
data = p.read_bytes()
old = b"import asyncio\r\nimport json\r\nimport logging\r\n"
new = b"import asyncio\r\nimport json\r\nimport logging\r\nimport threading\r\nimport time\r\n"
print("found:", old in data)
data = data.replace(old, new)
p.write_bytes(data)
print("done")
