from pathlib import Path
p = Path("src/gepaw/utils/logging.py")
data = p.read_bytes()
old = b"LOG_NAMESPACE = PROJECT_NAME.lower()"
new = b"LOG_NAMESPACE = \"gepaw\""
print("found:", old in data)
data = data.replace(old, new)
p.write_bytes(data)
print("done")
