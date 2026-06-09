from pathlib import Path
p = Path('src/gepaw/utils/logging.py')
t = p.read_text(encoding='utf-8')
if 'def get_logger' not in t:
    add = '''

def get_logger(name: str | None = None) -> "logging.Logger":
    """Return a logger under the gepaw namespace."""
    ns = LOG_NAMESPACE
    if not name:
        return logging.getLogger(ns)
    if not name.startswith(ns):
        return logging.getLogger(f"{ns}.{name}")
    return logging.getLogger(name)
'''
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
