"""Stub for agentscope_runtime.engine.schemas.exception."""
from __future__ import annotations


class AgentException(Exception):
    """Stub for `agentscope_runtime.engine.schemas.exception.AgentException`.

    Mirrors the real library's behaviour: keyword arguments are attached
    as attributes on the exception, but `message` is forwarded to the
    base `Exception` so `str(exc)` exposes it for assertion messages.
    """

    def __init__(self, *args, **kwargs) -> None:
        # Promote `message` kwarg (if any) to the positional message so
        # that `str(exc)` matches what callers expect.
        msg = kwargs.pop("message", None)
        if msg is None and args:
            msg = args[0]
            args = args[1:]
        super().__init__(msg, *args)
        for k, v in kwargs.items():
            setattr(self, k, v)


class AgentError(AgentException):
    pass


class AgentRunError(AgentException):
    pass


class ConfigurationException(AgentException):
    pass


class AgentRuntimeErrorException(AgentException):
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
    """Subclass that exposes `model_name` as the exception message."""

    def __init__(self, *args, **kwargs) -> None:
        model_name = kwargs.pop("model_name", None)
        super().__init__(*args, **kwargs)
        if model_name is not None:
            self.model_name = model_name
            # If the message is empty or None, set it to the model name so
            # `str(exc)` surfaces the model identifier (e.g. for
            # `pytest.raises(..., match=...)`).
            if not self.args or self.args[0] in (None, ""):
                self.args = (str(model_name),)


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
    """Subclass that exposes `model` (or model_name) as the message."""

    def __init__(self, *args, **kwargs) -> None:
        model = kwargs.pop("model", None) or kwargs.pop("model_name", None)
        super().__init__(*args, **kwargs)
        if model is not None:
            if not self.args or self.args[0] in (None, ""):
                self.args = (str(model),)


class ModelTimeoutException(AgentException):
    def __init__(self, *args, **kwargs) -> None:
        model = kwargs.pop("model", None)
        timeout = kwargs.pop("timeout", None)
        super().__init__(*args, **kwargs)
        if model is not None:
            if not self.args or self.args[0] in (None, ""):
                self.args = (str(model),)
        if timeout is not None:
            self.timeout = timeout


class ModelRateLimitException(AgentException):
    pass


class RequestTimeoutException(AgentException):
    pass


class UnauthorizedModelAccessException(AgentException):
    pass


class ModelQuotaExceededException(AgentException):
    pass


class ModelContextLengthExceededException(AgentException):
    pass


class UnknownAgentException(AgentException):
    pass


class ExternalServiceException(AgentException):
    pass


class RateLimitExceededException(AgentException):
    pass


class JSONException(AgentException):
    pass


class RateLimitError(AgentException):
    pass


class RequestError(AgentException):
    pass
