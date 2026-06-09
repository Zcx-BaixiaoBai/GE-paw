from pathlib import Path
p = Path('src/agentscope_runtime/engine/schemas/exception.py')
t = p.read_text(encoding='utf-8')
add = '''

class ModelExecutionException(AgentException):
    pass


class ModelTimeoutException(AgentException):
    pass


class ModelRateLimitException(AgentException):
    pass


class RequestTimeoutException(AgentException):
    pass
'''
t = t + add
p.write_text(t, encoding='utf-8')
print('added')
