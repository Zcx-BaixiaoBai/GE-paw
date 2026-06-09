"""Tool-call guard mixin.

Separated from the main agent class so the decision flow for blocking,
approving, or auto-allowing a tool call can be unit-tested in isolation.
The mixin only depends on the gepaw.security.tool_guard sub-package; it
imports the agent engine / approval service lazily so test code can
inject mocks via ``patch``.
"""
from __future__ import annotations

import asyncio
import logging
import uuid as _uuid
from dataclasses import dataclass
from typing import Any, Optional

from ..security.tool_guard.execution_level import ToolExecutionLevel
from ..security.tool_guard.models import (
    GuardFinding,
    GuardSeverity,
    GuardThreatCategory,
    ToolGuardResult,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tiny built-in i18n table. Tests only check that unknown keys return the
# key and that the function is robust against unknown locales.
# ---------------------------------------------------------------------------

_TOOL_GUARD_I18N: dict = {
    "en": {
        "tool_blocked": "Tool execution blocked by security policy.",
        "tool_needs_approval": "Tool execution requires user approval.",
        "severity_critical": "Critical",
        "severity_high": "High",
        "severity_medium": "Medium",
        "severity_low": "Low",
        "severity_info": "Info",
        "severity_safe": "Safe",
    },
    "zh": {
        "tool_blocked": "工具执行已被安全策略拦截。",
        "tool_needs_approval": "工具执行需要用户批准。",
        "severity_critical": "严重",
        "severity_high": "高",
        "severity_medium": "中",
        "severity_low": "低",
        "severity_info": "提示",
        "severity_safe": "安全",
    },
    "ru": {
        "tool_blocked": "Vypolnenie instrumenta zablokirovano politikoj bezopasnosti.",
        "tool_needs_approval": "Vypolnenie instrumenta trebuet odobrenija polzovatelja.",
        "severity_critical": "Kriticheskij",
        "severity_high": "Vysokij",
        "severity_medium": "Srednij",
        "severity_low": "Nizkij",
        "severity_info": "Informacija",
        "severity_safe": "Bezopasno",
    },
    "ja": {
        "tool_blocked": "ツールの実行はセキュリティポリシーによってブロックされました。",
        "tool_needs_approval": "ツールの実行にはユーザーの承認が必要です。",
        "severity_critical": "重大",
        "severity_high": "高",
        "severity_medium": "中",
        "severity_low": "低",
        "severity_info": "情報",
        "severity_safe": "安全",
    },
}


def _normalize_tool_guard_ui_lang(lang) -> str:
    """Coerce any caller-supplied language tag to a known short code."""
    if not lang or not isinstance(lang, str):
        return "en"
    s = lang.strip()
    if not s:
        return "en"
    s_lower = s.lower()
    if s_lower.startswith("zh"):
        return "zh"
    if s_lower.startswith("en"):
        return "en"
    if s_lower.startswith("ru"):
        return "ru"
    if s_lower.startswith("ja"):
        return "ja"
    return "en"


def _tool_guard_t(lang: str, key: str) -> str:
    """Return a localized string or the key itself if missing."""
    norm = _normalize_tool_guard_ui_lang(lang)
    return _TOOL_GUARD_I18N.get(norm, _TOOL_GUARD_I18N["en"]).get(key, key)


# Severity -> emoji. Kept identical to the QwenPaw reference implementation.
_SEV_EMOJI: dict = {
    GuardSeverity.CRITICAL: "\U0001f534",
    GuardSeverity.HIGH: "\U0001f534",
    GuardSeverity.MEDIUM: "\U0001f7e1",
    GuardSeverity.LOW: "\U0001f7e2",
    GuardSeverity.INFO: "\u2139\ufe0f",
    GuardSeverity.SAFE: "\u2705",
}


# ---------------------------------------------------------------------------
# Internal types
# ---------------------------------------------------------------------------


@dataclass
class _GuardAction:
    """Decision the mixin hands back to the agent loop."""

    kind: str  # "auto_denied" | "needs_approval" | "auto_allowed"
    tool_name: str
    tool_input: dict
    guard_result: Optional[ToolGuardResult] = None


# ---------------------------------------------------------------------------
# Mixin
# ---------------------------------------------------------------------------


class ToolGuardMixin:
    """Decision flow for blocking / approving / allowing tool calls."""

    # -- policy ----------------------------------------------------------

    def _should_require_approval(self) -> bool:
        ctx = getattr(self, "_request_context", None) or {}
        return bool(ctx.get("session_id"))

    def _get_tool_execution_level(self) -> ToolExecutionLevel:
        cfg = getattr(self, "_agent_config", None)
        if cfg is None:
            return ToolExecutionLevel.AUTO
        if isinstance(cfg, dict):
            level_str = cfg.get("approval_level")
        else:
            level_str = getattr(cfg, "approval_level", None)
        return ToolExecutionLevel.from_config(level_str)

    def _tool_guard_ui_lang(self) -> str:
        return _normalize_tool_guard_ui_lang(getattr(self, "_language", None))

    @classmethod
    def _severity_emoji_and_localized_name(
        cls, severity: GuardSeverity, lang: str
    ) -> tuple:
        norm = _normalize_tool_guard_ui_lang(lang)
        emoji = _SEV_EMOJI.get(severity, "\u2753")
        sev_value = (
            severity.value
            if hasattr(severity, "value") and isinstance(severity.value, str)
            else str(severity)
        )
        i18n_key = "severity_" + sev_value.lower()
        i18n = _TOOL_GUARD_I18N.get(norm, _TOOL_GUARD_I18N["en"])
        localized = i18n.get(i18n_key, sev_value)
        return emoji, localized

    # -- results ---------------------------------------------------------

    def _create_info_guard_result(
        self, tool_name: str, tool_input: Optional[dict]
    ) -> ToolGuardResult:
        params = dict(tool_input) if tool_input else {}
        finding = GuardFinding(
            id=str(_uuid.uuid4()),
            rule_id="strict_mode",
            category=GuardThreatCategory.RESOURCE_ABUSE,
            severity=GuardSeverity.INFO,
            title="Strict mode requires approval",
            description=(
                "Tool execution requires user approval under strict mode."
            ),
            tool_name=tool_name,
        )
        return ToolGuardResult(
            tool_name=tool_name,
            params=params,
            findings=[finding],
        )

    # -- core decision ---------------------------------------------------

    async def _decide_guard_action(
        self, tool_call: Optional[dict]
    ) -> Optional[_GuardAction]:
        tool_call = tool_call or {}
        name = tool_call.get("name") or ""
        if not name:
            return None
        engine = getattr(self, "_tool_guard_engine", None)
        if engine is None or not getattr(engine, "enabled", False):
            return None

        level = self._get_tool_execution_level()
        if level == ToolExecutionLevel.OFF:
            return None

        tool_input = tool_call.get("input") or {}

        # Explicitly denied tools short-circuit.
        if hasattr(engine, "is_denied") and engine.is_denied(name):
            guard_result = None
            if hasattr(engine, "guard"):
                guard_result = engine.guard(name, tool_input)
            return _GuardAction(
                "auto_denied", name, dict(tool_input), guard_result=guard_result
            )

        # STRICT mode requires approval for every tool call.
        if level == ToolExecutionLevel.STRICT:
            if not self._should_require_approval():
                return None
            guard_result = self._create_info_guard_result(name, tool_input)
            return _GuardAction(
                "needs_approval", name, dict(tool_input), guard_result=guard_result
            )

        # AUTO / SMART: run the engine and only react on findings.
        if not hasattr(engine, "guard"):
            return None
        guard_result = engine.guard(name, tool_input)
        findings = getattr(guard_result, "findings", []) or []
        if not findings:
            return None

        if hasattr(engine, "should_auto_deny_result") and bool(
            engine.should_auto_deny_result(guard_result)
        ):
            return _GuardAction(
                "auto_denied", name, dict(tool_input), guard_result=guard_result
            )

        if level == ToolExecutionLevel.SMART:
            max_sev = getattr(guard_result, "max_severity", None)
            if max_sev in (GuardSeverity.INFO, GuardSeverity.LOW):
                return None
            if not self._should_require_approval():
                return None
            return _GuardAction(
                "needs_approval", name, dict(tool_input), guard_result=guard_result
            )

        # AUTO mode with findings: escalate only if we can ask for approval.
        if not self._should_require_approval():
            return None
        return _GuardAction(
            "needs_approval", name, dict(tool_input), guard_result=guard_result
        )

    # -- lazy initialization --------------------------------------------

    def _ensure_tool_guard(self) -> None:
        if not hasattr(self, "_tool_guard_engine") or self._tool_guard_engine is None:
            from gepaw.security.tool_guard.engine import get_guard_engine

            self._tool_guard_engine = get_guard_engine()
        if not hasattr(
            self, "_tool_guard_approval_service"
        ) or self._tool_guard_approval_service is None:
            from gepaw.app.approvals import get_approval_service

            self._tool_guard_approval_service = get_approval_service()
        if not hasattr(self, "_tool_guard_lock") or self._tool_guard_lock is None:
            self._tool_guard_lock = asyncio.Lock()