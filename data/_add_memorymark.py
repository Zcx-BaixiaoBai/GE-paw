from pathlib import Path
p = Path('src/agentscope/agent/_react_agent.py')
t = p.read_text(encoding='utf-8')
add = '''

class _MemoryMark:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
'''
t = t + add
p.write_text(t, encoding='utf-8')
print('added')
