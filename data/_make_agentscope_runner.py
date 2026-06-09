import os
# Create agentscope_runtime.engine.runner stub
p = 'src/agentscope_runtime/engine/runner.py'
os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, 'w', encoding='utf-8').write('''\"\"\"Stub for agentscope_runtime.engine.runner.\"\"\"
from __future__ import annotations
from typing import Any, Optional


class AgentRunner:
    \"\"\"Stub for `agentscope_runtime.engine.runner.AgentRunner`.\"\"\"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    async def run(self, *args: Any, **kwargs: Any) -> Any:
        return None

    async def stream(self, *args: Any, **kwargs: Any) -> Any:
        yield None
''')
print('created')
