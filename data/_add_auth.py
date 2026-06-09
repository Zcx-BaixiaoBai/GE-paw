from pathlib import Path
p = Path('src/gepaw/exceptions.py')
t = p.read_text(encoding='utf-8')
if 'AuthError' not in t:
    add = '''

class AuthError(GepawError):
    """Raised on authentication failures."""


class PermissionError(GepawError):
    """Raised on permission denied."""


class ResourceNotFoundError(GepawError):
    """Raised when a required resource is missing."""
'''
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
