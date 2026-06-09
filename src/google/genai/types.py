"""Stub google.genai.types for gepaw test isolation."""
from __future__ import annotations

from typing import Any, Optional


class Content:
    """Placeholder for google.genai.types.Content."""

    def __init__(self, *, role: str = "user", parts: Optional[list] = None) -> None:
        self.role = role
        self.parts = parts or []


class Part:
    """Placeholder for google.genai.types.Part."""

    def __init__(self, *, text: str = "", **kwargs: Any) -> None:
        self.text = text
        self.kwargs = kwargs


class GenerateContentConfig:
    """Placeholder for google.genai.types.GenerateContentConfig."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs


class Tool:
    """Placeholder for google.genai.types.Tool."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs


class FunctionDeclaration:
    """Placeholder for google.genai.types.FunctionDeclaration."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs