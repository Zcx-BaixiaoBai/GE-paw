"""Small file-IO helpers used across gepaw.agents."""
from __future__ import annotations

from pathlib import Path
from typing import Union


def read_text_file_with_encoding_fallback(
    path: Union[str, Path],
    *,
    encodings: tuple = ("utf-8", "utf-8-sig", "gb18030", "latin-1"),
) -> str:
    """Read ``path`` as text, falling back through ``encodings`` on UnicodeError."""
    raw = Path(path).read_bytes()
    last_error = None
    for enc in encodings:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError as exc:
            last_error = exc
    if last_error is not None:
        raise last_error
    return ""