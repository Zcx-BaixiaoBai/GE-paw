from pathlib import Path
p = Path('src/acp/__init__.py')
t = p.read_text(encoding='utf-8')
if 'spawn_agent_process' not in t:
    t = t + '''

def spawn_agent_process(*args, **kwargs) -> Any:
    return None


def list_sessions(*args, **kwargs) -> Any:
    return []


def create_session(*args, **kwargs) -> Any:
    return None


def kill_process(*args, **kwargs) -> Any:
    return None
'''
    p.write_text(t, encoding='utf-8')
    print('added')
