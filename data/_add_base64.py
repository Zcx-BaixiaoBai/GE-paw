from pathlib import Path
p = Path('src/agentscope/message/__init__.py')
t = p.read_text(encoding='utf-8')
if 'Base64Source' not in t:
    t = t + '''

class Base64Source:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class URLSource:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
'''
    p.write_text(t, encoding='utf-8')
    print('added')
