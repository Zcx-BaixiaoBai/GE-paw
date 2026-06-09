"""Stub for agentscope_runtime.engine.schemas.exception."""
from __future__ import annotations


class AgentException(Exception):
    """Stub for `agentscope_runtime.engine.schemas.exception.AgentException`."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        for k, v in kwargs.items():
            setattr(self, k, v)


class AgentError(AgentException):
    pass


class AgentRunError(AgentException):
    pass


class ConfigurationException(AgentException):
    pass


class AgentRuntimeErrorException(AgentRuntimeError if False else AgentException):
    pass


class RunnerError(AgentException):
    pass


class SessionError(AgentException):
    pass


class AppBaseException(AgentException):
    pass


class AppException(AgentException):
    pass


class ServiceException(AgentException):
    pass


class ModelNotFoundException(AgentException):
    pass


class ModelError(AgentException):
    pass


class ModelAuthenticationError(AgentException):
    pass


class ToolNotFoundException(AgentException):
    pass


class ToolExecutionException(AgentException):
    pass


class ToolArgumentException(AgentException):
    pass


class ModelExecutionException(AgentException):
    pass


class ModelTimeoutException(AgentException):
    pass


class ModelRateLimitException(AgentException):
    pass


class RequestTimeoutException(AgentException):
    pass


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


class ModelQuotaExceededException(AgentException):
    pass


class RateLimitExceededException(AgentException):
    pass


class ModelContextLengthExceededException(AgentException):
    pass


class ExternalServiceException(AgentException):
    pass


class UnknownAgentException(AgentException):
    pass
