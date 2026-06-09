from pathlib import Path
p = Path('src/gepaw/constant.py')
t = p.read_text(encoding='utf-8')
add = '''
# Tool guard approval timeout
TOOL_GUARD_APPROVAL_TIMEOUT_SECONDS = 60
'''
if 'TOOL_GUARD_APPROVAL_TIMEOUT_SECONDS' not in t:
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
