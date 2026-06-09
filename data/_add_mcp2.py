from pathlib import Path
p = Path('src/agentscope/mcp.py')
t = p.read_text(encoding='utf-8')
add = '''

class StatefulClientBase:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    async def connect(self) -> None:
        return None

    async def close(self) -> None:
        return None

    async def list_tools(self) -> list:
        return []
'''
t = t + add
p.write_text(t, encoding='utf-8')
print('added')
