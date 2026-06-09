# -*- coding: utf-8 -*-
"""Factory for creating chat models and formatters.

This module provides a unified factory for creating chat model instances
and their corresponding formatters based on configuration.

Example:
    >>> from gepaw.agents.model_factory import create_model_and_formatter
    >>> model, formatter = create_model_and_formatter()
"""


import base64
import logging
import os
from typing import List, Tuple, Type, Any, Union, Optional
from urllib.parse import unquote, urlparse

from agentscope.formatter import FormatterBase, OpenAIChatFormatter
from agentscope.model import ChatModelBase, OpenAIChatModel

try:
    from agentscope.formatter import AnthropicChatFormatter
    from agentscope.model import AnthropicChatModel
except ImportError:  # pragma: no cover - compatibility fallback
    AnthropicChatFormatter = None
    AnthropicChatModel = None

try:
    from agentscope.formatter import GeminiChatFormatter
    from agentscope.model import GeminiChatModel
except ImportError:  # pragma: no cover - compatibility fallback
    GeminiChatFormatter = None
    GeminiChatModel = None

from .utils.message_request_normalizer import (
    normalize_messages_for_model_request,
)
from ..exceptions import ProviderError, ModelFormatterError


def _file_url_to_path(url: str) -> str:
    """Strip ``file://`` to a path.

    On Windows ``file:///C:/path`` becomes ``C:/path`` (not ``/C:/path``).
    Percent-decodes the path so non-ASCII filenames resolve correctly.
    """
    s = url.removeprefix("file://")
    if len(s) >= 3 and s.startswith("/") and s[1].isalpha() and s[2] == ":":
        s = s[1:]
    return unquote(s)


logger = logging.getLogger(__name__)

_SUPPORTED_IMAGE_EXTENSIONS: dict = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

_SUPPORTED_VIDEO_EXTENSIONS: dict = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mpeg": "video/mpeg",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska",
}


def _supports_multimodal_for_current_model() -> bool:
    """Best-effort lookup of current model multimodal support."""
    try:
        from .prompt import get_active_model_supports_multimodal

        return get_active_model_supports_multimodal()
    except Exception:  # pragma: no cover - config lookup safety
        logger.debug(
            "Falling back to multimodal=True during request-time "
            "message normalization",
            exc_info=True,
        )
        return True


def _normalize_messages_for_formatter(
    msgs: list,
    base_formatter_class: Type[FormatterBase],
    formatter_instance: Optional[FormatterBase] = None,
) -> tuple:
    """Return normalized messages and formatter-family flags.

    The returned booleans are
    ``(is_anthropic_formatter, is_gemini_formatter)``.
    All formatters receive a copied, normalized message list so
    request-time repair does not mutate stored history.
    """
    is_anthropic_formatter = AnthropicChatFormatter is not None and (
        issubclass(base_formatter_class, AnthropicChatFormatter)
    )
    is_gemini_formatter = GeminiChatFormatter is not None and (
        issubclass(base_formatter_class, GeminiChatFormatter)
    )
    supports_multimodal = _supports_multimodal_for_current_model()
    # gepaw attribute name (alias of the upstream qwenpaw flag) - tests
    # set this on the formatter instance to force-strip media for
    # multimodal-incapable runs even when the active model would
    # otherwise accept it.
    if getattr(formatter_instance, "_gepaw_force_strip_media", False):
        supports_multimodal = False

    if is_anthropic_formatter:
        target_family = "anthropic"
    elif is_gemini_formatter:
        target_family = "gemini"
    else:
        target_family = "openai"

    normalized_msgs = normalize_messages_for_model_request(
        msgs,
        supports_multimodal=supports_multimodal,
        target_family=target_family,
    )

    return normalized_msgs, is_anthropic_formatter, is_gemini_formatter


# TODO: remove after agentscope anthropic formatter updated
def _format_anthropic_media_block(block: dict) -> dict:
    """Format an image or video block for the Anthropic API.

    If the source is a URLSource pointing to a local file it will be
    converted to base64. Web URLs are passed through as-is.

    Args:
        block (`dict`): A block dict with ``type`` of ``"image"`` or ``"video"``.

    Returns:
        `dict`: Formatted block for the Anthropic API.

    Raises:
        `ModelFormatterError`: If the source type or media format is unsupported.
    """
    typ = block["type"]
    extensions = (
        _SUPPORTED_IMAGE_EXTENSIONS
        if typ == "image"
        else _SUPPORTED_VIDEO_EXTENSIONS
    )

    source = block["source"]

    if source["type"] == "base64":
        return {**block}

    url = source["url"]
    raw_url = _file_url_to_path(url)

    if os.path.exists(raw_url) and os.path.isfile(raw_url):
        ext = os.path.splitext(raw_url)[1].lower()
        media_type = extensions.get(ext)
        if media_type:
            with open(raw_url, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            return {
                "type": typ,
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": data,
                },
            }

    parsed_url = urlparse(raw_url)
    if parsed_url.scheme not in ("", "file"):
        return {
            "type": typ,
            "source": {
                "type": "url",
                "url": url,
            },
        }

    raise ModelFormatterError(
        message=(
            f'Invalid {typ} URL: "{url}". '
            "It should be a local file or a web URL."
        ),
    )


def _format_openai_video_block(video_block: dict) -> dict:
    """Format a video block for OpenAI-compatible APIs.

    Local files are converted to base64 data URLs; web URLs are passed
    through directly.

    Args:
        video_block (`dict`): The video block to format.

    Returns:
        `dict`: ``{"type": "video_url", "video_url": {"url": ...}}``.

    Raises:
        `ModelFormatterError`: If the source type or video format is unsupported.
    """
    source = video_block["source"]
    if source["type"] == "base64":
        media_type = source["media_type"]
        url = f"data:{media_type};base64,{source['data']}"
    elif source["type"] == "url":
        raw_url = _file_url_to_path(source["url"])
        if os.path.exists(raw_url) and os.path.isfile(raw_url):
            ext = os.path.splitext(raw_url)[1].lower()
            media_type = _SUPPORTED_VIDEO_EXTENSIONS.get(ext)
            if not media_type:
                raise ModelFormatterError(
                    f"Unsupported video extension: {ext}",
                )
            with open(raw_url, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            url = f"data:{media_type};base64,{data}"
        else:
            parsed = urlparse(raw_url)
            if parsed.scheme not in ("", "file"):
                url = source["url"]
            else:
                raise ModelFormatterError(
                    message=(
                        f"Invalid video URL: {source['url']}. "
                        "It should be a local file or a web URL."
                    ),
                )
    else:
        raise ModelFormatterError(
            message=f"Unsupported video source type: {source['type']}",
        )

    return {
        "type": "video_url",
        "video_url": {"url": url},
    }


def _replace_video_placeholders(
    messages: list,
    video_subs: dict,
) -> None:
    """Replace video placeholder text blocks with formatted video blocks."""
    for fmt_msg in messages:
        content = fmt_msg.get("content")
        if not isinstance(content, list):
            continue
        new_content = []
        for item in content:
            if (
                isinstance(item, dict)
                and item.get("type") == "text"
                and item.get("text") in video_subs
            ):
                new_content.append(
                    _format_openai_video_block(video_subs[item["text"]]),
                )
            else:
                new_content.append(item)
        fmt_msg["content"] = new_content


def _media_source_key(block: dict):
    """Extract a normalised path/URL from a media block for deduplication.

    Returns ``None`` for base64 sources (nothing to compare) or if no
    usable source URL is present.
    """
    source = block.get("source", {})
    if not isinstance(source, dict):
        source = {"type": "url", "url": str(source) if source else ""}
    if source.get("type") == "base64":
        return None
    url = source.get("url", "")
    if not url:
        return None
    raw = _file_url_to_path(url)
    if os.path.isabs(raw):
        return os.path.normpath(raw)
    return url


def _format_anthropic_output_items(
    output: list,
    seen_media=None,
) -> list:
    """Format a list of tool_result output blocks for Anthropic API.

    When *seen_media* is provided, media blocks whose source has already
    been encoded in a preceding top-level block are replaced with a
    lightweight text placeholder to avoid duplicating large base64 data.
    """
    result: list = []
    for item in output:
        item_type = item.get("type")

        if item_type == "file":
            source = item.get("source", {})
            if not isinstance(source, dict):
                source = {"type": "url", "url": str(source) if source else ""}
            file_url = source.get("url", "")
            filename = (
                item.get("filename")
                or file_url.rsplit("/", 1)[-1]
                or "unknown"
            )
            readable_path = file_url.removeprefix("file://")
            result.append(
                {
                    "type": "text",
                    "text": f"File ''{filename}'' is available at:"
                    f" {readable_path}",
                },
            )
            continue

        if item_type not in ("image", "video"):
            result.append(item)
            continue

        key = _media_source_key(item)
        if key and seen_media is not None and key in seen_media:
            result.append(
                {
                    "type": "text",
                    "text": (
                        f"[{item['type'].title()} omitted - same "
                        f"{item['type']} already visible above]"
                    ),
                },
            )
        else:
            result.append(_format_anthropic_media_block(item))
            if key and seen_media is not None:
                seen_media.add(key)

    return result


# TODO: remove after agentscope anthropic formatter updated
def _format_anthropic_messages(  # pylint: disable=too-many-branches
    msgs: list,
) -> list:
    """Format messages for the Anthropic API with image/video block support."""
    messages: list = []
    seen_media: set = set()
    for index, msg in enumerate(msgs):
        content_blocks: list = []

        for block in msg.get_content_blocks():
            typ = block.get("type")
            if typ in ["thinking", "text"]:
                content_blocks.append({**block})

            elif typ in ("image", "video"):
                key = _media_source_key(block)
                if key:
                    seen_media.add(key)
                content_blocks.append(
                    _format_anthropic_media_block(block),
                )

            elif typ == "tool_use":
                content_blocks.append(
                    {
                        "id": block.get("id"),
                        "type": "tool_use",
                        "name": block.get("name"),
                        "input": block.get("input", {}),
                    },
                )

            elif typ == "tool_result":
                output = block.get("output")
                if output is None:
                    content_value: list = [{"type": "text", "text": ""}]
                elif isinstance(output, list):
                    content_value = _format_anthropic_output_items(
                        output,
                        seen_media,
                    )
                else:
                    content_value = [{"type": "text", "text": str(output)}]
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.get("id"),
                                "content": content_value,
                            },
                        ],
                    },
                )

        if msg.role == "system" and index != 0:
            role = "user"
        else:
            role = msg.role

        msg_anthropic: dict = {
            "role": role,
            "content": content_blocks or "",
        }

        if msg_anthropic["content"] or msg_anthropic.get("tool_calls"):
            messages.append(msg_anthropic)

    return messages


# Mapping from chat model class to formatter class
_CHAT_MODEL_FORMATTER_MAP: dict = {
    OpenAIChatModel: OpenAIChatFormatter,
}
if AnthropicChatModel is not None and AnthropicChatFormatter is not None:
    _CHAT_MODEL_FORMATTER_MAP[AnthropicChatModel] = AnthropicChatFormatter
if GeminiChatModel is not None and GeminiChatFormatter is not None:
    _CHAT_MODEL_FORMATTER_MAP[GeminiChatModel] = GeminiChatFormatter


def _get_formatter_for_chat_model(
    chat_model_class: Type[ChatModelBase],
) -> Type[FormatterBase]:
    """Get the appropriate formatter class for a chat model."""
    return _CHAT_MODEL_FORMATTER_MAP.get(chat_model_class, OpenAIChatFormatter)


def _substitute_video_blocks(msgs: list) -> dict:
    """Replace video blocks in msgs with text placeholders."""
    video_subs: dict = {}
    for msg in msgs:
        if not isinstance(msg.content, list):
            continue
        for i, blk in enumerate(msg.content):
            if isinstance(blk, dict) and blk.get("type") == "video":
                ph = f"__GEPAW_VID_{id(blk)}__"
                video_subs[ph] = blk
                msg.content[i] = {"type": "text", "text": ph}
    return video_subs


def _restore_video_blocks(msgs: list, video_subs: dict) -> None:
    """Restore original video blocks in msgs after formatting."""
    for msg in msgs:
        if not isinstance(msg.content, list):
            continue
        for i, blk in enumerate(msg.content):
            if (
                isinstance(blk, dict)
                and blk.get("type") == "text"
                and blk.get("text") in video_subs
            ):
                msg.content[i] = video_subs[blk["text"]]


def _promote_tool_result_videos(msgs: list, messages: list) -> list:
    """Inject promoted video user messages after tool result messages."""
    promotions: dict = {}
    for msg in msgs:
        for block in msg.get_content_blocks():
            if block.get("type") != "tool_result":
                continue
            output = block.get("output")
            if not isinstance(output, list):
                continue
            videos = [
                (
                    item.get("source", {}).get("url", ""),
                    item,
                )
                for item in output
                if isinstance(item, dict) and item.get("type") == "video"
            ]
            if videos:
                promotions[block.get("id")] = (
                    block.get("name", ""),
                    videos,
                )

    if not promotions:
        return messages

    new_messages: list = []
    for fmt_msg in messages:
        new_messages.append(fmt_msg)
        tcid = fmt_msg.get("tool_call_id")
        if tcid not in promotions:
            continue
        tool_name, videos = promotions[tcid]
        promoted: list = [
            {
                "type": "text",
                "text": "<system-info>The following are "
                "the video contents from the tool "
                f"result of ''{tool_name}'':",
            },
        ]
        for url, vid_block in videos:
            promoted.append(
                {
                    "type": "text",
                    "text": f"\n- The video from ''{url}'': ",
                },
            )
            promoted.append(_format_openai_video_block(vid_block))
        promoted.append({"type": "text", "text": "</system-info>"})
        new_messages.append({"role": "user", "content": promoted})
    return new_messages


def _reorder_tool_and_promoted_messages(messages: list) -> list:
    """Move promoted user messages after all tool results in a sequence."""
    result: list = []
    i = 0
    while i < len(messages):
        msg = messages[i]
        if msg.get("role") == "assistant" and msg.get("tool_calls"):
            result.append(msg)
            i += 1
            tool_msgs: list = []
            promoted_msgs: list = []
            while i < len(messages) and messages[i].get("role") in (
                "tool",
                "user",
            ):
                if messages[i]["role"] == "tool":
                    tool_msgs.append(messages[i])
                else:
                    promoted_msgs.append(messages[i])
                i += 1
            result.extend(tool_msgs)
            result.extend(promoted_msgs)
        else:
            result.append(msg)
            i += 1
    return result


_MIME_FIXES: dict = {
    "image/jpg": "image/jpeg",
}


def _fix_image_mime_types(messages: list) -> None:
    """Fix non-standard MIME types in base64 data URLs in-place."""
    for msg in messages:
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            url = (block.get("image_url") or {}).get("url", "")
            if not isinstance(url, str):
                continue
            for bad, good in _MIME_FIXES.items():
                prefix = f"data:{bad};base64,"
                if url.startswith(prefix):
                    block["image_url"]["url"] = (
                        f"data:{good};base64," + url[len(prefix):]
                    )


# Block types that ``_fixup_media_list`` knows how to handle.
_MEDIA_BLOCK_TYPES = ("image", "audio", "video")
_FORMATTER_SKIPPED_TYPES = frozenset({"thinking", "file"})


def _fixup_media_list(items: list) -> None:
    """Replace missing media references and ``file`` blocks with placeholders.

    - When a media block points at a local file that no longer exists,
      replace it with a short text placeholder so the upstream formatter
      won't throw.
    - Converts ``file`` blocks to text placeholders, since neither the
      OpenAI nor the Anthropic top-level formatters accept ``file``
      blocks (the upstream OpenAI formatter silently drops them, which
      can drop the whole message if nothing else survives).
    - Recurses into ``tool_result`` output lists.
    """
    for i, block in enumerate(items):
        if not isinstance(block, dict):
            continue
        btype = block.get("type")
        if btype in _MEDIA_BLOCK_TYPES:
            source = block.get("source")
            if not (
                isinstance(source, dict)
                and source.get("type") == "url"
                and isinstance(source.get("url"), str)
            ):
                continue
            if source["url"].startswith("file://"):
                source["url"] = _file_url_to_path(source["url"])
            url = source["url"]
            if not url.startswith(
                ("http://", "https://", "data:"),
            ) and not os.path.exists(url):
                logger.warning(
                    "Media file no longer exists, "
                    "replacing with placeholder: %s",
                    url,
                )
                items[i] = {
                    "type": "text",
                    "text": (
                        f"[{btype.title()} unavailable"
                        f" - file deleted from disk]"
                    ),
                }
        elif btype == "file":
            source = block.get("source") or {}
            file_url = (
                source.get("url", "") if isinstance(source, dict) else ""
            )
            readable_path = (
                _file_url_to_path(file_url)
                if isinstance(file_url, str) and file_url.startswith("file://")
                else file_url
            )
            filename = (
                block.get("filename")
                or block.get("name")
                or (readable_path.rsplit("/", 1)[-1] if readable_path else "")
                or "file"
            )
            items[i] = {
                "type": "text",
                "text": (
                    f"File ''{filename}'' is available at: {readable_path}"
                    if readable_path
                    else f"File ''{filename}''"
                ),
            }
        elif btype == "tool_result":
            output = block.get("output")
            if isinstance(output, list):
                _fixup_media_list(output)


def _create_file_block_support_formatter(
    base_formatter_class: Type[FormatterBase],
) -> Type[FormatterBase]:
    """Create a formatter class with file block support."""

    class FileBlockSupportFormatter(base_formatter_class):
        """Formatter with file block support for tool results."""

        # pylint: disable=too-many-branches
        async def _format(self, msgs):
            """Sanitize tool messages, handle thinking, and relay extras."""
            (
                normalized_msgs,
                is_anthropic_formatter,
                _is_gemini_formatter,
            ) = _normalize_messages_for_formatter(
                msgs,
                base_formatter_class,
                self,
            )

            reasoning_contents: dict = {}
            extra_contents: dict = {}
            for msg in normalized_msgs:
                if msg.role != "assistant":
                    continue
                for block in msg.get_content_blocks():
                    if block.get("type") == "thinking":
                        thinking = block.get("thinking", "")
                        if thinking:
                            reasoning_contents[id(msg)] = thinking
                        break
                for block in msg.get_content_blocks():
                    if (
                        block.get("type") == "tool_use"
                        and "extra_content" in block
                    ):
                        extra_contents[block["id"]] = block["extra_content"]

            for msg in normalized_msgs:
                if isinstance(msg.content, list):
                    _fixup_media_list(msg.content)

            if is_anthropic_formatter:
                messages = _format_anthropic_messages(normalized_msgs)
            else:
                _needs_video = not _is_gemini_formatter
                video_subs: dict = {}
                if _needs_video:
                    video_subs = _substitute_video_blocks(normalized_msgs)

                messages = await super()._format(normalized_msgs)

                if video_subs:
                    _replace_video_placeholders(messages, video_subs)
                    _restore_video_blocks(normalized_msgs, video_subs)

                if _needs_video and getattr(
                    self,
                    "promote_tool_result_images",
                    False,
                ):
                    messages = _promote_tool_result_videos(
                        normalized_msgs,
                        messages,
                    )

            messages = _reorder_tool_and_promoted_messages(messages)

            _fix_image_mime_types(messages)

            if extra_contents and _is_gemini_formatter:
                for message in messages:
                    for tc in message.get("tool_calls", []):
                        ec = extra_contents.get(tc.get("id"))
                        if ec:
                            tc["extra_content"] = ec

            if reasoning_contents and not is_anthropic_formatter:
                aligned_reasoning = []
                for m in (
                    msg for msg in normalized_msgs if msg.role == "assistant"
                ):
                    is_dropped_by_formatter = (
                        isinstance(m.content, list)
                        and m.content
                        and all(
                            b.get("type") in _FORMATTER_SKIPPED_TYPES
                            for b in m.content
                        )
                    )
                    if not is_dropped_by_formatter:
                        aligned_reasoning.append(
                            reasoning_contents.get(id(m)),
                        )

                out_assistant = [
                    m for m in messages if m.get("role") == "assistant"
                ]

                if len(aligned_reasoning) != len(out_assistant):
                    logger.warning(
                        "Assistant message count mismatch after formatting "
                        "(%d expected survivors, %d produced); skipping "
                        "reasoning_content injection.",
                        len(aligned_reasoning),
                        len(out_assistant),
                    )
                else:
                    for out_msg, reasoning in zip(
                        out_assistant,
                        aligned_reasoning,
                    ):
                        if reasoning:
                            out_msg["reasoning_content"] = reasoning

            return messages

        def convert_tool_result_to_string(self, tool_result):
            """Extend parent class to support file blocks."""
            try:
                return super().convert_tool_result_to_string(tool_result)
            except Exception:
                return str(tool_result)

    FileBlockSupportFormatter.__name__ = (
        f"FileBlockSupport{base_formatter_class.__name__}"
    )
    return FileBlockSupportFormatter


def _strip_top_level_message_name(messages: list) -> list:
    """Strip top-level ``name`` from OpenAI chat messages."""
    for message in messages:
        message.pop("name", None)
    return messages


def create_model_and_formatter(
    agent_id: Optional[str] = None,
) -> Tuple:
    """Factory method to create model and formatter instances.

    Args:
        agent_id: Optional agent ID to load agent-specific model config.
            If None, tries to get from context, then falls back to global.

    Returns:
        Tuple of ``(model_instance, formatter_instance)``.
    """
    from ..app.agent_context import get_current_agent_id
    from ..config.config import load_agent_config
    from ..providers import ProviderManager
    from ..providers.retry_chat_model import (
        RetryChatModel,
        RetryConfig,
        RateLimitConfig,
    )
    from ..token_usage import TokenRecordingModelWrapper

    # Determine agent_id (parameter > context > None)
    if agent_id is None:
        try:
            agent_id = get_current_agent_id()
        except Exception:
            pass

    # Try to get agent-specific model first
    model_slot = None
    retry_config = None
    rate_limit_config = None
    if agent_id:
        try:
            agent_config = load_agent_config(agent_id)
            model_slot = agent_config.active_model
            retry_config = RetryConfig(
                enabled=agent_config.running.llm_retry_enabled,
                max_retries=agent_config.running.llm_max_retries,
                backoff_base=agent_config.running.llm_backoff_base,
                backoff_cap=agent_config.running.llm_backoff_cap,
            )
            rate_limit_config = RateLimitConfig(
                max_concurrent=agent_config.running.llm_max_concurrent,
                max_qpm=agent_config.running.llm_max_qpm,
                pause_seconds=agent_config.running.llm_rate_limit_pause,
                jitter_range=agent_config.running.llm_rate_limit_jitter,
                acquire_timeout=agent_config.running.llm_acquire_timeout,
            )
        except Exception:
            pass

    # Create chat model from agent-specific or global config
    if model_slot and model_slot.provider_id and model_slot.model:
        manager = ProviderManager.get_instance()
        provider = manager.get_provider(model_slot.provider_id)
        if provider is None:
            raise ProviderError(
                message=f"Provider ''{model_slot.provider_id}'' not found.",
            )

        model = provider.get_chat_model_instance(model_slot.model)
        provider_id = model_slot.provider_id
    else:
        # Fallback to global active model
        model = ProviderManager.get_active_chat_model()
        global_model = ProviderManager.get_instance().get_active_model()
        if not global_model:
            raise ProviderError(
                message=(
                    "No active model configured. "
                    "Please configure a model using ''gepaw models config'' "
                    "or set an agent-specific model."
                ),
            )
        provider_id = global_model.provider_id

    # Create the formatter based on the real model class
    formatter = _create_formatter_instance(model.__class__)

    # Wrap with retry logic for transient LLM API errors
    wrapped_model = TokenRecordingModelWrapper(provider_id, model)
    wrapped_model = RetryChatModel(
        wrapped_model,
        retry_config=retry_config,
        rate_limit_config=rate_limit_config,
    )

    return wrapped_model, formatter


def _create_formatter_instance(
    chat_model_class: Type[ChatModelBase],
) -> FormatterBase:
    """Create a formatter instance for the given chat model class."""
    base_formatter_class = _get_formatter_for_chat_model(chat_model_class)
    formatter_class = _create_file_block_support_formatter(
        base_formatter_class,
    )
    kwargs: dict = {}
    if issubclass(
        base_formatter_class,
        (OpenAIChatFormatter, GeminiChatFormatter),
    ):
        kwargs["promote_tool_result_images"] = True
    return formatter_class(**kwargs)


__all__ = [
    "create_model_and_formatter",
]