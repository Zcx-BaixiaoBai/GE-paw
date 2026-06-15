"""Per-agent markdown file manager.

Manages the small set of ``.md`` files that live either next to the
agent's working directory (project notes, scratchpads) or in the
``memory/`` sub-directory (session logs, summaries).
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Union

from ..utils.file_handling import read_text_file_with_encoding_fallback


def _md_filename(name: str) -> str:
    if not name:
        raise ValueError("markdown file name must not be empty")
    return name if name.lower().endswith(".md") else name + ".md"


def _describe(path: Path) -> dict:
    st = path.stat()
    return {
        "filename": path.name,
        "size": st.st_size,
        "path": str(path),
        "created_time": datetime.fromtimestamp(st.st_ctime).isoformat(),
        "modified_time": datetime.fromtimestamp(st.st_mtime).isoformat(),
    }


def _list_mds(directory: Path) -> list:
    if not directory.is_dir():
        return []
    return [
        _describe(p)
        for p in sorted(directory.iterdir())
        if p.is_file() and p.suffix.lower() == ".md"
    ]


class AgentMdManager:
    """Read / write markdown files in the agent workspace and memory dirs."""

    def __init__(self, working_dir: Union[str, Path], agent_id: str = "") -> None:
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir = self.working_dir / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.agent_id = agent_id

    def list_working_mds(self) -> list:
        return _list_mds(self.working_dir)

    def read_working_md(self, name: str) -> str:
        path = self.working_dir / _md_filename(name)
        if not path.exists():
            raise FileNotFoundError(str(path))
        return read_text_file_with_encoding_fallback(path).strip()

    def write_working_md(self, name: str, content: str) -> Path:
        path = self.working_dir / _md_filename(name)
        path.write_text(content, encoding="utf-8")
        return path

    def list_memory_mds(self) -> list:
        return _list_mds(self.memory_dir)

    def read_memory_md(self, name: str) -> str:
        path = self.memory_dir / _md_filename(name)
        if not path.exists():
            raise FileNotFoundError(str(path))
        return read_text_file_with_encoding_fallback(path).strip()

    def write_memory_md(self, name: str, content: str) -> Path:
        path = self.memory_dir / _md_filename(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path