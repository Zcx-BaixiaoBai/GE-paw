from pathlib import Path
import re
p = Path("src/agentscope/tool.py")
data = p.read_text()
old = """    def get_json_schemas(self) -> list:
        return []"""
new = """    def get_json_schemas(self) -> list:
        schemas: list = []
        for func in self.tools:
            name = getattr(func, "__name__", "") or ""
            doc = (getattr(func, "__doc__", "") or "").strip()
            schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": doc,
                    "parameters": {"type": "object", "properties": {}},
                },
            })
        return schemas"""
print("found:", old in data)
data = data.replace(old, new)
p.write_text(data)
print("done")
