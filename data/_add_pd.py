from pathlib import Path
p = Path('src/gepaw/exceptions.py')
t = p.read_text(encoding='utf-8')
if 'PermissionDeniedError' not in t:
    t = t + '''

class PermissionDeniedError(Exception):
    \"\"\"Raised when an action is denied.\"\"\"


class ValidationError(Exception):
    \"\"\"Raised on input validation failures.\"\"\"


class ConfigurationError(Exception):
    \"\"\"Raised on configuration errors.\"\"\"


class SkillError(Exception):
    \"\"\"Raised on skill-related errors.\"\"\"


class ProviderError(Exception):
    \"\"\"Raised on provider-related errors.\"\"\"


class ToolNotFoundError(Exception):
    \"\"\"Raised when a tool is not found.\"\"\"


class ChannelError(Exception):
    \"\"\"Raised on channel-related errors.\"\"\"


class ToolError(Exception):
    \"\"\"Raised on tool execution errors.\"\"\"


class AgentError(Exception):
    \"\"\"Raised on agent-related errors.\"\"\"


class SessionError(Exception):
    \"\"\"Raised on session errors.\"\"\"


class InitializationError(Exception):
    \"\"\"Raised on initialization errors.\"\"\"


class TimeoutError_(Exception):
    \"\"\"Raised on timeout (avoid shadowing builtin).\"\"\"
'''
    p.write_text(t, encoding='utf-8')
    print('added')
