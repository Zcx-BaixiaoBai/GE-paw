"""Tool guard engine - orchestrates all registered guardians.

This is a self-contained subset of the original QwenPaw engine. It
covers only the surfaces exercised by gepaw tests:

- lazy module-level singleton (``get_guard_engine``)
- ``_guard_enabled()`` free function (env > config > True default)
- ``ToolGuardEngine`` class with explicit ``guardians`` and ``enabled``
  constructor parameters, public properties for the resolved tool
  sets, registration helpers, and a ``guard`` method that aggregates
  findings from all configured guardians with per-guardian error
  isolation.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Iterable, List, Optional, Set


from gepaw.constant import EnvVarLoader


logger = logging.getLogger(__name__)


_TRUE_STRINGS = {"true", "1", "yes"}


def _guard_enabled() -> bool:
    """Return whether tool-call guarding is enabled.

    Priority: env var > config.json > default (True).
    """
    env_val = EnvVarLoader.get_str("GEPAW_TOOL_GUARD_ENABLED")
    if env_val:
        return env_val.lower() in _TRUE_STRINGS

    try:
        from gepaw.config import load_config
        cfg = load_config()
        return bool(cfg.security.tool_guard.enabled)
    except Exception:
        return True


class ToolGuardEngine:
    """Orchestrates pre-tool-call security guarding.

    Parameters
    ----------
    guardians:
        Explicit list of guardians.  When ``None``, the default set
        is loaded lazily.
    enabled:
        Force enable/disable regardless of env / config.
    """

    def __init__(
        self,
        guardians: Optional[Iterable[Any]] = None,
        *,
        enabled: Optional[bool] = None,
    ) -> None:
        self._enabled = enabled if enabled is not None else _guard_enabled()

        if guardians is not None:
            self._guardians: List[Any] = list(guardians)
        else:
            self._guardians = self._default_guardians()

        self._reload_tool_sets()

    # ------------------------------------------------------------------
    # Default guardians
    # ------------------------------------------------------------------

    @staticmethod
    def _default_guardians() -> List[Any]:
        """Return the default set of guardians (best effort)."""
        guardians: List[Any] = []
        try:
            from .guardians.file_guardian import FilePathToolGuardian
            guardians.append(FilePathToolGuardian())
        except Exception as exc:  # pragma: no cover
            logger.warning(
                "Failed to initialise FilePathToolGuardian: %s", exc,
            )
        try:
            from .guardians.rule_guardian import RuleBasedToolGuardian
            guardians.append(RuleBasedToolGuardian())
        except Exception as exc:  # pragma: no cover
            logger.warning(
                "Failed to initialise RuleBasedToolGuardian: %s", exc,
            )
        return guardians

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_guardian(self, guardian: Any) -> None:
        self._guardians.append(guardian)
        logger.debug("Registered tool guardian: %s", guardian.name)

    def unregister_guardian(self, name: str) -> bool:
        before = len(self._guardians)
        self._guardians = [g for g in self._guardians if g.name != name]
        return len(self._guardians) < before

    @property
    def guardian_names(self) -> List[str]:
        return [g.name for g in self._guardians]

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = bool(value)

    @property
    def guarded_tools(self) -> Optional[Set[str]]:
        return self._guarded_tools

    @property
    def denied_tools(self) -> Set[str]:
        return self._denied_tools

    @property
    def auto_denied_rules(self) -> Set[str]:
        return self._auto_denied_rules

    def _reload_tool_sets(self) -> None:
        """Refresh guarded/denied/auto-denied sets from utils + config."""
        from .utils import (
            resolve_auto_denied_rules,
            resolve_denied_tools,
            resolve_guarded_tools,
        )

        self._guarded_tools = resolve_guarded_tools()
        self._denied_tools = resolve_denied_tools()
        self._auto_denied_rules = resolve_auto_denied_rules()

    def reload_rules(self) -> None:
        """Reload guardian rules and refresh guarded/denied tool sets."""
        for g in self._guardians:
            reload_fn = getattr(g, "reload", None)
            if reload_fn is not None:
                try:
                    reload_fn()
                except Exception:  # noqa: BLE001
                    logger.exception(
                        "reload failed for guardian %s", g.name,
                    )
        self._reload_tool_sets()

    def is_denied(self, tool_name: str) -> bool:
        return tool_name in self._denied_tools

    def should_auto_deny_result(self, result: Any) -> bool:
        """``True`` if any finding's rule_id is in the auto-deny set."""
        if (
            result is None
            or not getattr(result, "findings", None)
            or not self._auto_denied_rules
        ):
            return False
        return any(
            f.rule_id in self._auto_denied_rules for f in result.findings
        )

    def is_guarded(self, tool_name: str) -> bool:
        if self._guarded_tools is None:
            return True
        return tool_name in self._guarded_tools

    # ------------------------------------------------------------------
    # Core interface
    # ------------------------------------------------------------------

    def guard(
        self,
        tool_name: str,
        params: Optional[dict] = None,
        *,
        only_always_run: bool = False,
    ) -> Any:
        """Run all configured guardians and aggregate findings."""
        from .models import ToolGuardResult

        if not self._enabled:
            return None

        params = params or {}
        start = time.monotonic()
        result = ToolGuardResult(
            tool_name=tool_name,
            params=params,
            guard_duration_seconds=0.0,
        )

        for g in self._guardians:
            if only_always_run and not getattr(g, "always_run", False):
                continue
            try:
                findings = g.guard(tool_name, params) or []
                result.findings.extend(findings)
                result.guardians_used.append(g.name)
            except Exception as exc:  # noqa: BLE001 - guardian errors isolated
                result.guardians_failed.append(
                    {"name": g.name, "error": str(exc)},
                )
                logger.warning(
                    "tool guardian %s raised during guard: %s",
                    g.name, exc,
                )

        result.guard_duration_seconds = time.monotonic() - start
        return result


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------


_engine_instance: Optional[ToolGuardEngine] = None


def get_guard_engine() -> ToolGuardEngine:
    """Return the lazy module-level ToolGuardEngine singleton."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ToolGuardEngine()
    return _engine_instance