from pathlib import Path
# Add AppBaseException
p = Path('src/agentscope_runtime/engine/schemas/exception.py')
t = p.read_text(encoding='utf-8')
add = '''

class AppBaseException(AgentException):
    pass


class AppException(AgentException):
    pass


class ServiceException(AgentException):
    pass
'''
t = t + add
p.write_text(t, encoding='utf-8')
print('exceptions added')

# Add ChatUsage to agentscope.model._model_usage
p2 = Path('src/agentscope/model/_model_usage.py')
t2 = p2.read_text(encoding='utf-8')
add2 = '''

class ChatUsage:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class _ModelUsage:
    pass
'''
t2 = t2 + add2
p2.write_text(t2, encoding='utf-8')
print('ChatUsage added')
