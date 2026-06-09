from pathlib import Path
p = Path('src/gepaw/exceptions.py')
t = p.read_text(encoding='utf-8')
old = '''class AuthError(GepawError):
    \"\"\"Raised on authentication failures.\"\"\"


class PermissionError(GepawError):
    \"\"\"Raised on permission denied.\"\"\"


class ResourceNotFoundError(GepawError):
    \"\"\"Raised when a required resource is missing.\"\"\"'''
new = '''class AuthError(Exception):
    \"\"\"Raised on authentication failures.\"\"\"


class PermissionError(Exception):
    \"\"\"Raised on permission denied.\"\"\"


class ResourceNotFoundError(Exception):
    \"\"\"Raised when a required resource is missing.\"\"\"'''
if old in t:
    t = t.replace(old, new, 1)
    p.write_text(t, encoding='utf-8')
    print('fixed')
else:
    print('not found')
