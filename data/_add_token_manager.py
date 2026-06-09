from pathlib import Path
p = Path('src/gepaw/token_usage/__init__.py')
t = p.read_text(encoding='utf-8')
if 'get_token_usage_manager' not in t:
    t = t + '''

from .manager import get_token_usage_manager  # noqa: E402, F401
'''
    p.write_text(t, encoding='utf-8')
    print('added')
