"""Default and override model cost table (USD per 1K tokens)."""
from __future__ import annotations

from typing import Dict


_DEFAULTS: Dict[str, Dict[str, int]] = {
    "gpt-4o": {"prompt": 250, "completion": 1000},
    "gpt-4o-mini": {"prompt": 15, "completion": 60},
    "gpt-4-turbo": {"prompt": 1000, "completion": 3000},
    "gpt-3.5-turbo": {"prompt": 50, "completion": 150},
    "o1": {"prompt": 1500, "completion": 6000},
    "o1-mini": {"prompt": 300, "completion": 1200},
    "o3-mini": {"prompt": 110, "completion": 440},
    "claude-3-5-sonnet": {"prompt": 300, "completion": 1500},
    "claude-3-haiku": {"prompt": 25, "completion": 125},
    "local-stub": {"prompt": 0, "completion": 0},
    "stub": {"prompt": 0, "completion": 0},
}

_OVERRIDES: Dict[str, Dict[str, int]] = {}


def set_override(model: str, prompt_cents_per_1k: int, completion_cents_per_1k: int) -> None:
    _OVERRIDES[model] = {"prompt": int(prompt_cents_per_1k), "completion": int(completion_cents_per_1k)}


def clear_override(model: str) -> None:
    _OVERRIDES.pop(model, None)


def list_overrides() -> Dict[str, Dict[str, int]]:
    return dict(_OVERRIDES)


def quote_for(model: str) -> Dict[str, int]:
    m = (model or "").strip()
    if m in _OVERRIDES:
        return dict(_OVERRIDES[m])
    if m in _DEFAULTS:
        return dict(_DEFAULTS[m])
    for k, v in _DEFAULTS.items():
        if m.startswith(k):
            return dict(v)
    return {"prompt": 0, "completion": 0}


def compute_cost_cents(model: str, prompt_tokens: int, completion_tokens: int) -> int:
    q = quote_for(model)
    p = max(0, int(prompt_tokens))
    c = max(0, int(completion_tokens))
    return int(round(p * q["prompt"] / 1000.0 + c * q["completion"] / 1000.0))


def known_models() -> list[str]:
    return sorted(set(list(_DEFAULTS.keys()) + list(_OVERRIDES.keys())))
