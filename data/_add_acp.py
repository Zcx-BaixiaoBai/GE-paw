from pathlib import Path
p = Path('src/acp.py')
t = p.read_text(encoding='utf-8')
if 'update_tool_call' not in t:
    add = '''

def update_tool_call(*args, **kwargs) -> Any:
    return None
'''
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
