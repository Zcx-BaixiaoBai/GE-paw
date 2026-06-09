"""GE-paw token usage tracking package.

Public API:
    record_usage(...)   - write a TokenUsageLog row (call this once per LLM call)
    summarize / by_day / by_user / by_model / month_to_date / last_days
                        - read-side aggregation helpers
    compute_cost_cents, quote_for, list_overrides, set_override, known_models
                        - cost table helpers
"""
from .cost_table import (  # noqa: F401
    compute_cost_cents,
    quote_for,
    list_overrides,
    set_override,
    clear_override,
    known_models,
)
from .model_wrapper import record_usage, TokenRecordingModelWrapper  # noqa: F401
from . import manager  # noqa: F401

__all__ = [
    "record_usage",
    "TokenRecordingModelWrapper",
    "compute_cost_cents",
    "quote_for",
    "list_overrides",
    "set_override",
    "clear_override",
    "known_models",
    "manager",
]


from .manager import get_token_usage_manager  # noqa: E402, F401
