from pathlib import Path
p = Path('src/gepaw/constant.py')
t = p.read_text(encoding='utf-8')
add = '''
# Memory directory (mirrors qwenpaw defaults)
from pathlib import Path
MEMORY_DIR = (WORKING_DIR / "memory") if 'WORKING_DIR' in dir() else Path.home() / ".gepaw" / "memory"
'''
if 'MEMORY_DIR =' not in t:
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
