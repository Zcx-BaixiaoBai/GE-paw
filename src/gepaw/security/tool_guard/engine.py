"""gepaw.security.tool_guard.engine: stub engine for tool-call guard tests.

A real implementation would scan the tool call against the rule set and
guardian pipeline. The v0.1 stub only exists so test code that does
``patch("gepaw.security.tool_guard.engine.get_guard_engine")`` can resolve
the module. The mixin only calls it lazily.
"""
def get_guard_engine():
    raise NotImplementedError("tool guard engine not configured")
