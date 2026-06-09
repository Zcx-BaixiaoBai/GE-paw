import os
# Create browser_use stub
p = 'src/gepaw/agents/tools/browser_use.py'
os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, 'w', encoding='utf-8').write('''\"\"\"Browser-use tool stub.\"\"\"
from __future__ import annotations
from typing import Any


async def browse_url(*args: Any, **kwargs: Any) -> str:
    return ''


async def click(*args: Any, **kwargs: Any) -> str:
    return ''


async def type_text(*args: Any, **kwargs: Any) -> str:
    return ''


async def get_text(*args: Any, **kwargs: Any) -> str:
    return ''
''')
print('created')
