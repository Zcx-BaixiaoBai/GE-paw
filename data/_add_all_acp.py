from pathlib import Path
# Add allowed/denied outcome to acp.schema
p = Path('src/acp/schema.py')
t = p.read_text(encoding='utf-8')
extras = ['AllowedOutcome', 'DeniedOutcome']
adds = []
for e in extras:
    if e not in t:
        adds.append(f'''

class {e}:
    option_id = ''
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
''')
if adds:
    t = t + ''.join(adds)
    p.write_text(t, encoding='utf-8')
    print('added', len(adds))
