"""Stub for questionary CLI prompt library."""
from __future__ import annotations
from typing import Any, Optional


def confirm(message: str, default: bool = True, **kwargs) -> 'Choice':
    return Choice(answer=default)


def text(message: str, default: str = '', **kwargs) -> 'Choice':
    return Choice(answer=default)


def select(message: str, choices, default: Any = None, **kwargs) -> 'Choice':
    return Choice(answer=default if default is not None else (choices[0] if choices else None))


def path(message: str, default: str = '', **kwargs) -> 'Choice':
    return Choice(answer=default)


def password(message: str, **kwargs) -> 'Choice':
    return Choice(answer='')


class Choice:
    def __init__(self, answer: Any = None) -> None:
        self.answer = answer

    def ask(self) -> Any:
        return self.answer


def ask(prompt) -> Any:
    return prompt.ask() if hasattr(prompt, 'ask') else None


# form / Style stubs
class Style:
    def __init__(self, *args, **kwargs) -> None:
        pass


# form module
def form(*fields) -> 'Form':
    return Form()


class Form:
    def ask(self) -> dict:
        return {}
