from pathlib import Path
p = Path('src/agentscope/mcp.py')
t = p.read_text(encoding='utf-8')
add = '''

class MCPToolFunction:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    async def call(self, *args, **kwargs) -> Any:
        return None
'''
t = t + add
p.write_text(t, encoding='utf-8')
print('added')
