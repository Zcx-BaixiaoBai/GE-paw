from pathlib import Path
p = Path('src/gepaw/exceptions.py')
t = p.read_text(encoding='utf-8')
old = '''class ChannelError(Exception):
    """Raised on channel-related errors."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        for k, v in kwargs.items():
            setattr(self, k, v)'''
new = '''class ChannelError(Exception):
    """Raised on channel-related errors."""
    def __init__(self, *args, **kwargs):
        # Prefer 'message' kwarg as the primary exception text so that
        # `str(exc)` exposes it for `pytest.raises(..., match=...)`.
        msg = kwargs.pop("message", None)
        if msg is None and args:
            msg = args[0]
            args = args[1:]
        super().__init__(msg, *args)
        for k, v in kwargs.items():
            setattr(self, k, v)'''
if old in t:
    t = t.replace(old, new, 1)
    p.write_text(t, encoding='utf-8')
    print('fixed ChannelError')
else:
    print('not found')
