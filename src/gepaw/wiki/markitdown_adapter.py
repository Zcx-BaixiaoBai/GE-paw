"""将非 md 源文件转 markdown。"""
from __future__ import annotations

import os
import tempfile
from typing import Optional

from ..utils.logging import get_logger

logger = get_logger("wiki.markitdown")


def convert_to_markdown(filename: str, data: bytes) -> str:
    name = filename.lower()
    if name.endswith((".md", ".markdown", ".txt")):
        return data.decode("utf-8", errors="replace")
    if name.endswith((".html", ".htm")):
        return _html_to_md(data)
    if name.endswith((".csv", ".tsv")):
        return _table_to_md(data, sep="\t" if name.endswith(".tsv") else ",")
    try:
        from markitdown import MarkItDown
    except Exception:
        logger.warning("markitdown 未安装，返回纯文本占位")
        return f"# {filename}\n\n> 该文件类型需要 markitdown 依赖才能正确解析。\n\n```\n{data[:4000].decode('utf-8', errors='replace')}\n```\n"
    try:
        suffix = os.path.splitext(filename)[1] or ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            md = MarkItDown()
            result = md.convert(tmp_path)
            return getattr(result, "text_content", str(result)) or ""
        finally:
            try: os.remove(tmp_path)
            except OSError: pass
    except Exception as e:
        logger.warning("markitdown 转换失败: %s", e)
        return f"# {filename}\n\n> 转换失败：{e}\n"


def _html_to_md(data: bytes) -> str:
    try:
        import html2text
    except Exception:
        return data.decode("utf-8", errors="replace")
    h = html2text.HTML2Text(); h.body_width = 0; h.ignore_links = False
    return h.handle(data.decode("utf-8", errors="replace"))


def _table_to_md(data: bytes, sep: str) -> str:
    import csv
    import io
    text = data.decode("utf-8", errors="replace")
    reader = csv.reader(io.StringIO(text), delimiter=sep)
    rows = [r for r in reader if r]
    if not rows:
        return ""
    head = rows[0]
    lines = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
    for r in rows[1:]:
        r = (r + [""] * len(head))[:len(head)]
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)
