from pathlib import Path
p = Path('src/gepaw/constant.py')
t = p.read_text(encoding='utf-8')
add = '''

# Upload media max size in MB
UPLOAD_MAX_SIZE_MB = 50
'''
if 'UPLOAD_MAX_SIZE_MB' not in t:
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
