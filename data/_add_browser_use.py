from pathlib import Path
p = Path('src/gepaw/agents/tools/__init__.py')
t = p.read_text(encoding='utf-8')
if 'browser_use' not in t:
    t = t + '''

try:
    from . import browser_use  # noqa: F401
except ImportError:
    pass
'''
    p.write_text(t, encoding='utf-8')
    print('added')
