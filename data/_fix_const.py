from pathlib import Path
p = Path('src/gepaw/constant.py')
t = p.read_text(encoding='utf-8')
old = '# Memory directory (mirrors qwenpaw defaults)\nfrom pathlib import Path\nMEMORY_DIR = (WORKING_DIR / "memory") if '+"'"+'WORKING_DIR'+ "'"+' in dir() else Path.home() / ".gepaw" / "memory"'
new = '# Memory directory (mirrors qwenpaw defaults)\nfrom pathlib import Path as _Path\nMEMORY_DIR = (WORKING_DIR / "memory") if isinstance(WORKING_DIR, _Path) else _Path.home() / ".gepaw" / "memory"'
if old in t:
    t = t.replace(old, new)
    p.write_text(t, encoding='utf-8')
    print('fixed')
else:
    print('not found, try simpler approach')
