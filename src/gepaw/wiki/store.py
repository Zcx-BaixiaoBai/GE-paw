"""Wiki 语料存储抽象：当前实现为本地文件系统，预留 S3/OSS 接口。"""
from __future__ import annotations

import os
import re
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from ..models import WikiCorpus
from ..utils.logging import get_logger

logger = get_logger("wiki.store")


@dataclass
class FsNode:
    name: str
    path: str
    type: str
    size: int
    mtime: float
    sha256: Optional[str] = None


def _safe_rel(path: str) -> str:
    p = path.replace("\\", "/").strip("/")
    if not p:
        return ""
    parts: list[str] = []
    for seg in p.split("/"):
        if seg in ("", "."):
            continue
        if seg == "..":
            raise PermissionError("路径越界")
        parts.append(seg)
    rel = "/".join(parts)
    if rel.split("/", 1)[0] not in ("wiki", "raw", "graph"):
        raise PermissionError("路径越界")
    return rel


class WikiStore(ABC):
    def __init__(self, corpus: WikiCorpus) -> None:
        self.corpus = corpus

    @abstractmethod
    def put_raw(self, name: str, data: bytes) -> str: ...

    @abstractmethod
    def get_raw(self, rel_path: str) -> bytes: ...

    @abstractmethod
    def list_tree(self, sub: str = "wiki", max_depth: int = 6) -> List[FsNode]: ...

    @abstractmethod
    def read_text(self, rel_path: str, max_bytes: int) -> str: ...

    @abstractmethod
    def exists(self, rel_path: str) -> bool: ...

    @abstractmethod
    def write_text(self, rel_path: str, content: str) -> None: ...

    @abstractmethod
    def purge(self) -> None: ...


class FilesystemWikiStore(WikiStore):
    _NAME_SAFE = re.compile(r"[^\w.\-]+", re.UNICODE)

    def __init__(self, corpus: WikiCorpus) -> None:
        super().__init__(corpus)
        self.root = Path(corpus.root_path).resolve()
        (self.root / "raw").mkdir(parents=True, exist_ok=True)
        (self.root / "wiki").mkdir(parents=True, exist_ok=True)
        (self.root / "graph").mkdir(parents=True, exist_ok=True)

    def _resolve(self, rel: str) -> Path:
        rel = _safe_rel(rel)
        p = (self.root / rel).resolve() if rel else self.root
        if not str(p).startswith(str(self.root)):
            raise PermissionError("路径越界")
        return p

    def _safe_name(self, name: str) -> str:
        base = os.path.basename(name)
        base = self._NAME_SAFE.sub("_", base)
        return base or "untitled"

    def put_raw(self, name: str, data: bytes) -> str:
        safe = self._safe_name(name)
        target = self.root / "raw" / safe
        if target.exists():
            stem = target.stem
            suf = target.suffix
            i = 1
            while True:
                cand = self.root / "raw" / f"{stem}_{i}{suf}"
                if not cand.exists():
                    target = cand
                    break
                i += 1
        target.write_bytes(data)
        return f"raw/{target.name}"

    def get_raw(self, rel_path: str) -> bytes:
        return self._resolve(rel_path).read_bytes()

    def read_text(self, rel_path: str, max_bytes: int) -> str:
        p = self._resolve(rel_path)
        with p.open("rb") as f:
            data = f.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError(f"文件超过大小限制 ({max_bytes} bytes)")
        return data.decode("utf-8", errors="replace")

    def list_tree(self, sub: str = "wiki", max_depth: int = 6) -> List[FsNode]:
        if sub not in ("wiki", "raw", "graph"):
            raise PermissionError("sub 必须为 wiki/raw/graph")
        start = (self.root / sub).resolve()
        nodes: List[FsNode] = []
        if not start.exists():
            return nodes
        for root, dirs, files in os.walk(start):
            depth = str(root).count(os.sep) - str(start).count(os.sep)
            if depth > max_depth:
                dirs[:] = []
                continue
            rel_root = Path(root).relative_to(self.root).as_posix()
            for d in sorted(dirs):
                p = Path(root) / d
                nodes.append(FsNode(
                    name=d, path=f"{rel_root}/{d}", type="dir",
                    size=0, mtime=p.stat().st_mtime,
                ))
            for f in sorted(files):
                p = Path(root) / f
                nodes.append(FsNode(
                    name=f, path=f"{rel_root}/{f}", type="file",
                    size=p.stat().st_size, mtime=p.stat().st_mtime,
                ))
        return nodes

    def write_text(self, rel_path: str, content: str) -> None:
        p = self._resolve(rel_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def exists(self, rel_path: str) -> bool:
        try:
            return self._resolve(rel_path).exists()
        except PermissionError:
            return False

    def purge(self) -> None:
        for sub in ("raw", "wiki", "graph"):
            p = self.root / sub
            if p.exists():
                shutil.rmtree(p, ignore_errors=True)
            p.mkdir(parents=True, exist_ok=True)


def get_wiki_store(corpus: WikiCorpus) -> WikiStore:
    kind = (corpus.storage_kind or "fs").lower()
    if kind == "fs":
        return FilesystemWikiStore(corpus)
    raise NotImplementedError(f"暂不支持的存储类型: {kind}")
