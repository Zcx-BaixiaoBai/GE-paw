from pathlib import Path
p = Path('src/acp/__init__.py')
t = p.read_text(encoding='utf-8')
add = '''

def session_notification(*args, **kwargs) -> Any:
    return None


def request_permission(*args, **kwargs) -> Any:
    return None


def ext_method(*args, **kwargs) -> Any:
    return None
'''
t = t + add
p.write_text(t, encoding='utf-8')
print('added')
