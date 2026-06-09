import os
# Create agentscope.tool stub
p = 'src/agentscope/tool.py'
open(p, 'w', encoding='utf-8').write('''\"\"\"Stub for agentscope.tool.\"\"\"
from __future__ import annotations
from typing import Any


async def execute_python_code(*args, **kwargs) -> Any:
    return ''


async def view_text_file(*args, **kwargs) -> Any:
    return ''


async def write_text_file(*args, **kwargs) -> Any:
    return ''
''')
print('created')
