"""Stub for telegram.constants."""
from __future__ import annotations


class _Const:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class ParseMode:
    MARKDOWN = _Const('MarkdownV2')
    MARKDOWN_V2 = _Const('MarkdownV2')
    HTML = _Const('HTML')
    PLAIN = _Const('')
