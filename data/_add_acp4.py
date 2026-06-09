from pathlib import Path
p = Path('src/acp/__init__.py')
t = p.read_text(encoding='utf-8')
extras = ['RequestError', 'AuthenticationRequired', 'PermissionDenied', 'McpError']
adds = []
for e in extras:
    if e not in t:
        adds.append(f'''

class {e}(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        for k, v in kwargs.items():
            setattr(self, k, v)
''')
if adds:
    t = t + ''.join(adds)
    p.write_text(t, encoding='utf-8')
    print('added', len(adds))
else:
    print('exists')
