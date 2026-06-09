from pathlib import Path
p = Path("src/gepaw/token_usage/__init__.py")
data = p.read_text()
old = "from .model_wrapper import record_usage  # noqa: F401"
new = "from .model_wrapper import record_usage, TokenRecordingModelWrapper  # noqa: F401"
print("found:", old in data)
data = data.replace(old, new)
# Also add to __all__
old2 = '''    "record_usage",'''
new2 = '''    "record_usage",
    "TokenRecordingModelWrapper",'''
data = data.replace(old2, new2)
p.write_text(data)
print("done")
