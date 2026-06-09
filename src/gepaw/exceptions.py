"""GE-paw 自定义异常。"""
from typing import Any, Optional


class GepawError(Exception):
    """所有 GE-paw 异常的基类。"""

    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, message: str, *, code: Optional[str] = None, status_code: Optional[int] = None, detail: Optional[Any] = None) -> None:
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code
        if status_code is not None:
            self.status_code = status_code
        self.detail = detail


class NotFoundError(GepawError):
    status_code = 404
    code = "not_found"


class PermissionDeniedError(GepawError):
    status_code = 403
    code = "permission_denied"


class AuthError(GepawError):
    status_code = 401
    code = "auth_error"


class ValidationError(GepawError):
    status_code = 400
    code = "validation_error"


class ConflictError(GepawError):
    status_code = 409
    code = "conflict"


class RateLimitError(GepawError):
    status_code = 429
    code = "rate_limited"


class ProviderError(GepawError):
    status_code = 502
    code = "provider_error"


class ModelFormatterError(GepawError):
    status_code = 500
    code = "model_formatter_error"


class SystemCommandException(GepawError):
    status_code = 500
    code = "system_command_error"


class ChannelError(GepawError):
    status_code = 502
    code = "channel_error"


class AgentStateError(GepawError):
    status_code = 409
    code = "agent_state_error"


class SkillsError(GepawError):
    status_code = 500
    code = "skills_error"