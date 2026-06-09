from pathlib import Path
p = Path('src/acp/__init__.py')
t = p.read_text(encoding='utf-8')
if 'PROTOCOL_VERSION' not in t:
    t = t + '''

PROTOCOL_VERSION = 1
'''
    p.write_text(t, encoding='utf-8')
    print('added')
