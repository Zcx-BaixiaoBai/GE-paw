from pathlib import Path
p = Path('src/gepaw/exceptions.py')
t = p.read_text(encoding='utf-8')
if 'class ChannelError' in t and 'def __init__' not in t.split('class ChannelError')[1].split('class')[0]:
    old = 'class ChannelError(Exception):'
    new = 'class ChannelError(Exception):\n    def __init__(self, *args, **kwargs):\n        super().__init__(*args)\n        for k, v in kwargs.items():\n            setattr(self, k, v)'
    t = t.replace(old, new, 1)
    p.write_text(t, encoding='utf-8')
    print('fixed')
