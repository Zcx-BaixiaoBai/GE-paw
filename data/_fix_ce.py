from pathlib import Path
p = Path('src/gepaw/exceptions.py')
t = p.read_text(encoding='utf-8')
old = 'class ChannelError(Exception):\n    """Raised on channel-related errors."""'
new = 'class ChannelError(Exception):\n    """Raised on channel-related errors."""\n    def __init__(self, *args, **kwargs):\n        super().__init__(*args)\n        for k, v in kwargs.items():\n            setattr(self, k, v)'
if old in t:
    t = t.replace(old, new, 1)
    p.write_text(t, encoding='utf-8')
    print('fixed')
