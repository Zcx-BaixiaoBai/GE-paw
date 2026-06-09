import os
# Add more exceptions
p = 'src/agentscope_runtime/engine/schemas/exception.py'
t = open(p, encoding='utf-8').read()
add = '''

class ConfigurationException(AgentException):
    pass


class AgentRuntimeErrorException(AgentRuntimeError if False else AgentException):
    pass


class RunnerError(AgentException):
    pass


class SessionError(AgentException):
    pass
'''
t = t + add
open(p, 'w', encoding='utf-8').write(t)
print('exceptions extended')

# Create agentscope.model._model_usage stub
pp = 'src/agentscope/model/_model_usage.py'
os.makedirs(os.path.dirname(pp), exist_ok=True)
open(pp, 'w', encoding='utf-8').write('''\"\"\"Stub for agentscope.model._model_usage.\"\"\"
from __future__ import annotations
from typing import Any


class ModelUsage:
    \"\"\"Stub ModelUsage class.\"\"\"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
''')
print('model_usage stub created')
