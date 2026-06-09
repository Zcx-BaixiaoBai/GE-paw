from pathlib import Path
p = Path('src/agentscope_runtime/engine/schemas/exception.py')
t = p.read_text(encoding='utf-8')
add = '''

class UnauthorizedModelAccessException(AgentException):
    pass


class TokenUsageException(AgentException):
    pass


class SessionNotFoundException(AgentException):
    pass


class AgentExecutionException(AgentException):
    pass


class UserNotFoundException(AgentException):
    pass
'''
t = t + add
p.write_text(t, encoding='utf-8')
print('added')
