"""Stub: agentscope_runtime.engine.schemas.exception for gepaw tests."""
from __future__ import annotations

from typing import Any


class _BaseAgentError(Exception):
    """Common base for agent-runtime exceptions."""

    def __init__(self, message: str = "", **kwargs: Any) -> None:
        super().__init__(message)
        for k, v in kwargs.items():
            setattr(self, k, v)


class AgentRuntimeErrorException(_BaseAgentError):
    """Generic agent runtime error."""


class ModelNotFoundException(_BaseAgentError):
    """Raised when a referenced model is not registered."""


class AgentNotFoundException(_BaseAgentError):
    """Raised when a referenced agent is not found."""


class RequestRejectedException(_BaseAgentError):
    """Raised when a request is rejected."""


class ExternalServiceException(_BaseAgentError):
    """Raised when an external service is unavailable."""


class ConfigurationException(_BaseAgentError):
    """Raised when a configuration value is missing or invalid."""


class JsonOutputParsingException(_BaseAgentError):
    """Raised when JSON output cannot be parsed."""


class AuthorizationException(_BaseAgentError):
    """Raised when an operation is not authorised."""


class RateLimitExceededException(_BaseAgentError):
    """Raised when a rate limit is exceeded."""


class QuotaExceededException(_BaseAgentError):
    """Raised when a quota is exceeded."""
class AppBaseException(Exception):
    """Generic application base exception used across gepaw routes."""