from pathlib import Path
p = Path("src/gepaw/app/channels/registry.py")
data = p.read_bytes()
old = b"CHANNEL_KINDS = (\r\n    \'telegram\',\r\n    \'discord\',"
new = b"CHANNEL_KINDS = (\r\n    \'echo\',\r\n    \'telegram\',\r\n    \'discord\',"
print("found:", old in data)
data = data.replace(old, new)
p.write_bytes(data)
print("done")
