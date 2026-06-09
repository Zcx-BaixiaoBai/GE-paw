"""Stub OpenAIChatModel for gepaw test isolation."""
from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any, AsyncIterator, Dict, List, Optional

from .chat_model_base import ChatModelBase


def _coerce_arguments(arguments: Any) -> Any:
    """Parse tool-call arguments as JSON when possible.

    OpenAI emits tool-call arguments as JSON strings; tests in gepaw
    assert against the decoded dict.
    """
    if isinstance(arguments, str):
        try:
            return json.loads(arguments)
        except (TypeError, ValueError):
            return arguments
    return arguments


def _content_blocks_from_chunk(chunk: Any) -> list[dict[str, Any]]:
    """Translate a single OpenAI-style chunk into a list of content blocks."""
    blocks: list[dict[str, Any]] = []
    choices = getattr(chunk, "choices", None) or []
    for choice in choices:
        delta = getattr(choice, "delta", None)
        if delta is None:
            continue
        text = getattr(delta, "content", None)
        if text:
            blocks.append({"type": "text", "text": text})
        for tool_call in getattr(delta, "tool_calls", None) or []:
            function = getattr(tool_call, "function", None)
            name = getattr(function, "name", None) if function else None
            arguments = getattr(function, "arguments", None) if function else None
            blocks.append(
                {
                    "type": "tool_use",
                    "id": getattr(tool_call, "id", None),
                    "name": name,
                    "input": _coerce_arguments(arguments),
                }
            )
    return blocks


def _make_chat_response(chunk: Any) -> Any:
    """Wrap a chunk into a stub `ChatResponse`-like object."""
    return SimpleNamespace(
        content=_content_blocks_from_chunk(chunk),
        usage=getattr(chunk, "usage", None),
        chunk=chunk,
    )


def _iter_chunks(src: Any) -> Any:
    """Yield chunks from a stream-like object.

    Handles async-context-manager streams (`async with src: ...`),
    bare async iterables (`async for x in src: ...`), and plain
    iterables.  Anything else is treated as a single chunk.
    """
    if hasattr(src, "__aenter__") and hasattr(src, "__aexit__"):

        class _StreamCtx:
            def __init__(self, outer):
                self._outer = outer
                self._inner: Any = None

            async def __aenter__(self):
                self._inner = await self._outer.__aenter__()
                return self

            async def __aexit__(self, exc_type, exc, tb):
                return await self._outer.__aexit__(exc_type, exc, tb)

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self._inner is None:
                    raise StopAsyncIteration
                try:
                    return await self._inner.__anext__()
                except StopAsyncIteration:
                    raise

        return _StreamCtx(src)

    return src


class OpenAIChatModel(ChatModelBase):
    """Placeholder for the real OpenAI chat model."""

    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        )
        self.generate_kwargs: Dict[str, Any] = dict(kwargs)

    async def __call__(  # type: ignore[no-untyped-def]
        self,
        messages: List[Any],
        **kwargs: Any,
    ) -> Any:
        raise NotImplementedError

    async def stream(  # type: ignore[no-untyped-def]
        self,
        messages: List[Any],
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        raise NotImplementedError
        yield  # pragma: no cover

    async def _parse_openai_stream_response(
        self,
        start_datetime: Any,
        stream: Any = None,
        response: Any = None,
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        src = stream if stream is not None else response
        if src is None:
            return

        ctx = _iter_chunks(src)

        if hasattr(ctx, "__aenter__") and hasattr(ctx, "__aexit__"):
            async with ctx as opened:
                async for chunk in opened:
                    yield _make_chat_response(chunk)
                return

        if hasattr(ctx, "__aiter__"):
            async for chunk in ctx:
                yield _make_chat_response(chunk)
            return

        for chunk in ctx:
            yield _make_chat_response(chunk)
