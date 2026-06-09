"""Wiki 流水线：ingest / compile / lint / query。"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from ..models import WikiCorpus, WikiQueryLog, WikiSource
from ..utils.logging import get_logger
from .llm_client import chat_for_org
from .markitdown_adapter import convert_to_markdown
from .store import FilesystemWikiStore, get_wiki_store

logger = get_logger("wiki.pipeline")

_SLUG_RE = re.compile(r"[^a-z0-9\u4e00-\u9fff]+")


def _slugify(name: str) -> str:
    stem = Path(name).stem
    s = _SLUG_RE.sub("-", stem.lower()).strip("-")
    return s[:80] or "untitled"


def run_ingest(corpus: WikiCorpus, source: WikiSource, db: Session) -> None:
    store = get_wiki_store(corpus)
    assert isinstance(store, FilesystemWikiStore)
    raw_bytes = store.get_raw(source.path)
    md = convert_to_markdown(Path(source.path).name, raw_bytes)
    title = source.title or Path(source.path).stem
    slug = _slugify(Path(source.path).stem)
    today = datetime.now(timezone.utc).replace(tzinfo=None).strftime("%Y-%m-%d")
    frontmatter = (
        "---\n"
        f"title: {title}\n"
        "type: source\n"
        "tags: []\n"
        f"sources: [{Path(source.path).name}]\n"
        f"last_updated: {today}\n"
        "---\n\n"
    )
    body = _truncate(md, 50000)
    summary = _make_summary(md)
    page = frontmatter + f"# {title}\n\n> 来源: `{source.path}`\n\n## 摘要\n\n{summary}\n\n## 全文\n\n{body}\n"
    rel_page = f"wiki/sources/{slug}.md"
    store.write_text(rel_page, page)
    source.status = "ingested"
    source.last_ingested_at = datetime.now(timezone.utc).replace(tzinfo=None)
    source.error = None
    db.commit()
    logger.info("ingested %s -> %s", source.path, rel_page)


def run_compile(corpus: WikiCorpus, db: Session) -> int:
    store = get_wiki_store(corpus)
    rows = db.query(WikiSource).filter(WikiSource.corpus_id == corpus.id, WikiSource.status == "ingested").all()
    sources_dir = Path(store.root) / "wiki" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now(timezone.utc).replace(tzinfo=None).strftime("%Y-%m-%d")
    lines: List[str] = ["---", "title: \"Wiki Index\"", "type: index", f"last_updated: {today}", "---\n", "# Wiki Index\n"]
    for s in rows:
        slug = _slugify(Path(s.path).stem)
        lines.append(f"- [[{slug}]] —{s.title or Path(s.path).name}")
    store.write_text("wiki/index.md", "\n".join(lines) + "\n")

    titles = [s.title or Path(s.path).stem for s in rows[:30]]
    overview = (
        "---\n"
        "title: \"Overview\"\n"
        "type: overview\n"
        f"last_updated: {today}" +
        "---\n\n"
        "# 总览\n\n"
        f"共有 **{len(rows)}** 个源。当前主题包括：{', '.join(titles)}。\n"
    )
    store.write_text("wiki/overview.md", overview)
    db.commit()
    return len(rows)


def run_lint(corpus: WikiCorpus, db: Session) -> Dict[str, Any]:
    store = get_wiki_store(corpus)
    pages = [n for n in store.list_tree("wiki") if n.type == "file" and n.path.startswith("wiki/sources/")]
    links_re = re.compile(r"\[\[([^\]]+)\]\]")
    body_by_page: Dict[str, str] = {}
    for p in pages:
        try:
            body_by_page[p.path] = store.read_text(p.path, 200000)
        except Exception:
            body_by_page[p.path] = ""
    referenced: set = set()
    for body in body_by_page.values():
        for m in links_re.findall(body):
            referenced.add(m.strip())
    orphans: List[str] = []
    for p in pages:
        slug = Path(p.path).stem
        if slug not in referenced:
            orphans.append(p.path)
    return {"orphans": orphans, "total_pages": len(pages)}


def run_query(corpus: WikiCorpus, db: Session, *, question: str, user_id: Optional[str] = None, top_k: int = 5) -> Dict[str, Any]:
    t0 = time.time()
    store = get_wiki_store(corpus)
    pages = [n for n in store.list_tree("wiki") if n.type == "file" and n.path.startswith("wiki/sources/")]
    q = (question or "").strip()
    if not q:
        return {"answer": "", "citations": [], "tokens_in": 0, "tokens_out": 0, "latency_ms": 0}

    scored: List[Tuple[float, str, str]] = []
    tokens = re.findall(r"[\w\u4e00-\u9fff]+", q.lower())
    for p in pages:
        try:
            body = store.read_text(p.path, 200000)
        except Exception:
            continue
        body_l = body.lower()
        score = 0
        for t in tokens:
            if not t:
                continue
            score += body_l.count(t)
        try:
            head = "\n".join(body.splitlines()[:6]).lower()
            for t in tokens:
                if t and t in head:
                    score += 5
        except Exception:
            pass
        if score > 0:
            snippet = _best_snippet(body, tokens)
            scored.append((float(score), p.path, snippet))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]
    citations: List[Dict[str, Any]] = [{"path": p, "snippet": s, "score": sc} for sc, p, s in top]
    if not top:
        answer = "知识库中未找到与该问题匹配的内容。"
        result_in, result_out = 0, 0
    else:
        context_blocks: List[str] = []
        for sc, p, s in top:
            context_blocks.append(f"### 来源: {p}\n\n{s}\n")
        context = "\n\n".join(context_blocks)
        prompt = (
            "你是 GE-paw 问答助手。请仅根据下面提供的「来源片段」回答用户问题，"
            "回答末尾用「引用」一节列出[path#snippet] 形式的来源。\n\n"
            f"用户问题: {q}\n\n来源片段:\n{context}\n"
        )
        res = chat_for_org(db, corpus.org_id, [
            {"role": "system", "content": "你是一个严谨的问答助手，只基于提供的资料回答。"},
            {"role": "user", "content": prompt},
        ], temperature=0.2, max_tokens=1024)
        answer = res.content or ""
        result_in, result_out = res.prompt_tokens, res.completion_tokens
    latency = int((time.time() - t0) * 1000)
    db.add(WikiQueryLog(
        corpus_id=corpus.id, user_id=user_id, query=q,
        answer_excerpt=answer[:500], citations_json=json.dumps(citations, ensure_ascii=False),
        tokens_in=result_in, tokens_out=result_out, latency_ms=latency,
    ))
    db.commit()
    return {"answer": answer, "citations": citations, "tokens_in": result_in, "tokens_out": result_out, "latency_ms": latency}


def _truncate(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n] + "\n\n> (内容被截断"


def _make_summary(md: str) -> str:
    for line in md.splitlines():
        s = line.strip()
        if not s: continue
        if s.startswith("#"): continue
        return s[:400]
    return (md[:400]).strip()


def _best_snippet(body: str, tokens: List[str]) -> str:
    if not tokens:
        return body[:600]
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        low = s.lower()
        if any(t and t in low for t in tokens):
            return s[:600]
    return body[:600]
