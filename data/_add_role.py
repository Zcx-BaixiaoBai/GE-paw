from pathlib import Path
p = Path('src/agentscope_runtime/engine/schemas/agent_schemas.py')
t = p.read_text(encoding='utf-8')
if 'class Role' not in t:
    add = '''


class Role(str, Enum):
    """Role of the message author."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    DEVELOPER = "developer"
'''
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
