from pathlib import Path
p = Path('src/gepaw/utils/logging.py')
t = p.read_text(encoding='utf-8')
old = 'def setup_logger(level: int | str = logging.INFO):'
new = 'def setup_logger(level: int | str = logging.INFO, *, log_path=None):'
if old in t:
    t = t.replace(old, new, 1)
    p.write_text(t, encoding='utf-8')
    print('fixed')
