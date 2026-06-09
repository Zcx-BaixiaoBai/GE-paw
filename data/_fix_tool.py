from pathlib import Path
p = Path('src/agentscope/tool.py')
t = p.read_text(encoding='utf-8')
add = '''

class Toolkit:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.tools: list = []

    def register_tool_function(self, func) -> None:
        self.tools.append(func)

    def get_json_schemas(self) -> list:
        return []


class ToolResponse:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._data = dict(kwargs)
        self.content = kwargs.get('content', '')

    def to_dict(self) -> dict:
        return dict(self._data)
'''
t = t + add
p.write_text(t, encoding='utf-8')
print('added')
