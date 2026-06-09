"""Stub for json_repair library."""
from __future__ import annotations

import json
from typing import Any


def repair_json(json_str: str, return_objects: bool = False) -> Any:
    """Best-effort stub: try to load, fall back to ``{"raw": ...}``."""
    try:
        return json.loads(json_str)
    except (TypeError, ValueError):
        if return_objects:
            return {"_raw": json_str}
        return json_str