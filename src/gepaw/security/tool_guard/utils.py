"""Tool-guard utility helpers.

* Configuration resolution: which tools to guard, which to deny, and
  which rules auto-deny.
* Structured logging of guard findings.
"""
from __future__ import annotations

import logging
from typing import Any, Iterable, List, Optional, Set, Union


from gepaw.constant import EnvVarLoader


logger = logging.getLogger(__name__)


_DEFAULT_GUARDED_TOOLS: frozenset = frozenset(
    {
        "execute_shell_command",
        "read_file",
        "write_file",
        "edit_file",
        "append_file",
        "send_file_to_user",
        "view_text_file",
        "write_text_file",
    },
)


_DISABLE_TOKENS = {"none", "off", "false", "0"}


def _parse_guarded_tokens(tokens: Iterable[str]) -> Optional[Set[str]]:
    """Parse guarded tool tokens into a scope set.

    ``None`` means "guard all tools".  An empty set means "guard
    nothing".  Recognised disable tokens: ``none``, ``off``, ``false``,
    ``0`` (case-insensitive).  ``all`` and ``*`` are recognised
    "guard-everything" sentinels.
    """
    normalized = {item.strip() for item in tokens if item and item.strip()}
    if not normalized:
        return set()

    lowered = {item.lower() for item in normalized}
    if "*" in lowered or "all" in lowered:
        return None
    if lowered.issubset(_DISABLE_TOKENS):
        return set()

    return normalized


def _load_config_tool_guard() -> Any:
    """Load the ``tool_guard`` section of the config, or return ``None``."""
    try:
        from gepaw.config import load_config
        return load_config().security.tool_guard
    except Exception:
        return None


def resolve_guarded_tools(
    user_defined: Optional[Union[Set[str], List[str], tuple]] = None,
) -> Optional[Set[str]]:
    """Resolve which tools fall in the guard scope.

    Priority:
    1. ``user_defined`` (constructor-supplied)
    2. ``GEPAW_TOOL_GUARD_TOOLS`` env var
    3. ``config.json`` -> ``security.tool_guard.guarded_tools``
    4. built-in high-risk default set
    """
    if user_defined is not None:
        return _parse_guarded_tokens(user_defined)

    raw = EnvVarLoader.get_str("GEPAW_TOOL_GUARD_TOOLS")
    if raw:
        normalized = raw.strip().lower()
        if normalized in {"*", "all"}:
            return None
        if normalized in {"", "none", "off", "false", "0"}:
            return set()
        return _parse_guarded_tokens(raw.split(","))

    cfg = _load_config_tool_guard()
    if cfg is not None and cfg.guarded_tools is not None:
        return _parse_guarded_tokens(cfg.guarded_tools)

    return set(_DEFAULT_GUARDED_TOOLS)


def resolve_denied_tools(
    user_defined: Optional[Union[Set[str], List[str], tuple]] = None,
) -> Set[str]:
    """Resolve which tools are unconditionally denied (no approval offered)."""
    if user_defined is not None:
        return set(user_defined)

    raw = EnvVarLoader.get_str("GEPAW_TOOL_GUARD_DENIED_TOOLS")
    if raw:
        return {t.strip() for t in raw.split(",") if t.strip()}

    cfg = _load_config_tool_guard()
    if cfg is not None and cfg.denied_tools:
        return set(cfg.denied_tools)

    return set()


def resolve_auto_denied_rules(
    user_defined: Optional[Union[Set[str], List[str], tuple]] = None,
) -> Set[str]:
    """Resolve which rule IDs should trigger unconditional auto-deny."""
    if user_defined is not None:
        return {r.strip() for r in user_defined if r and r.strip()}

    raw = EnvVarLoader.get_str("GEPAW_TOOL_GUARD_AUTO_DENIED_RULES")
    if raw:
        return {r.strip() for r in raw.split(",") if r.strip()}

    cfg = _load_config_tool_guard()
    if cfg is not None and cfg.auto_denied_rules:
        return {r.strip() for r in cfg.auto_denied_rules if r.strip()}

    return set()


def log_findings(tool_name: str, result: Any) -> None:
    """Emit structured logs for each finding and a summary line."""
    from .models import GuardSeverity

    _HIGH = (GuardSeverity.CRITICAL, GuardSeverity.HIGH)

    for finding in result.findings:
        log_fn = logger.warning if finding.severity in _HIGH else logger.info
        log_fn(
            "[TOOL GUARD] %s | tool=%s param=%s rule=%s | %s | matched=%r",
            finding.severity.value,
            tool_name,
            finding.param_name or "*",
            finding.rule_id,
            finding.description,
            finding.matched_value,
        )

    summary_fn = (
        logger.warning if result.max_severity in _HIGH else logger.info
    )
    summary_fn(
        "[TOOL GUARD] Summary for tool %r: %d finding(s), "
        "max_severity=%s, duration=%.3fs",
        tool_name,
        result.findings_count,
        result.max_severity.value,
        result.guard_duration_seconds,
    )