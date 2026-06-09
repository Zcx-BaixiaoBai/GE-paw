from pathlib import Path
p = Path('src/gepaw/app/_app.py')
t = p.read_text(encoding='utf-8')
old = 'setup_logger(s.log_level, LOG_FILE_PATH)'
new = 'setup_logger(s.log_level, log_path=LOG_FILE_PATH)'
if old in t:
    t = t.replace(old, new, 1)
    p.write_text(t, encoding='utf-8')
    print('fixed')
else:
    print('not found')
