"""Unit tests for the wiki pipeline ingest / compile / lint / query path."""
from __future__ import annotations

import os
import shutil
import tempfile
import uuid
import pytest
from sqlalchemy import create_engine

from gepaw.app.db import init_db, session_scope, Base
from gepaw.app import db as _dbmod
from gepaw.app.settings import get_settings
from gepaw.wiki.store import FilesystemWikiStore
from gepaw.wiki.pipeline import run_ingest, run_compile, run_lint, run_query
from gepaw.models.wiki import WikiCorpus, WikiSource
from gepaw.models.identity import Org


@pytest.fixture
def ctx(monkeypatch):
    get_settings.cache_clear()
    if _dbmod._engine is not None:
        try:
            _dbmod._engine.dispose(close=True)
        except Exception:
            pass
    _dbmod._engine = None
    _dbmod._SessionLocal = None
    tmp = tempfile.mkdtemp(prefix="gepaw-pipe-" + uuid.uuid4().hex[:6] + "-")
    db = os.path.join(tmp, "test.db")
    monkeypatch.setenv("GEPAW_DATABASE_URL", "sqlite:///" + db)
    monkeypatch.setenv("GEPAW_DATA_DIR", tmp)
    get_settings.cache_clear()
    eng = create_engine("sqlite:///" + db)
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)
    eng.dispose()
    init_db()
    org_id = "o-" + uuid.uuid4().hex[:8]
    corpus_id = "c-" + uuid.uuid4().hex[:8]
    with session_scope() as db:
        db.add(Org(id=org_id, name="Org1", slug="slug-" + uuid.uuid4().hex[:8]))
    with session_scope() as db:
        db.add(WikiCorpus(id=corpus_id, org_id=org_id, name="default",
                          root_path=os.path.join(tmp, "wiki"), storage_kind="fs"))
    yield tmp, org_id
    try:
        _dbmod._engine.dispose(close=True)
    except Exception:
        pass
    _dbmod._engine = None
    _dbmod._SessionLocal = None
    shutil.rmtree(tmp, ignore_errors=True)


def test_ingest_then_query_stub(ctx):
    tmp, org_id = ctx
    corpus_id = None
    with session_scope() as db:
        corpus = db.query(WikiCorpus).filter(WikiCorpus.org_id == org_id).first()
        corpus_id = corpus.id
        store = FilesystemWikiStore(corpus)
        store.write_text("raw/notes.md", "# Notes\n## Topic\nGE-paw is a multi-tenant agent platform.")
        src = WikiSource(
            corpus_id=corpus.id, sha256="x" * 64, path="raw/notes.md",
            size_bytes=64, mime="text/markdown", title="notes.md", status="pending",
        )
        db.add(src)
        db.commit()
        src_id = src.id

    with session_scope() as db:
        corpus = db.query(WikiCorpus).filter(WikiCorpus.org_id == org_id).first()
        src = db.query(WikiSource).get(src_id)
        run_ingest(corpus, src, db)

    with session_scope() as db:
        corpus = db.query(WikiCorpus).filter(WikiCorpus.org_id == org_id).first()
        src = db.query(WikiSource).get(src_id)
        assert src.status == "ingested"
        c = run_compile(corpus, db)
        assert isinstance(c, int) and c >= 1
        l = run_lint(corpus, db)
        assert "total_pages" in l
        q = run_query(corpus, db, question="GE-paw", user_id="u1", top_k=3)
        assert "answer" in q
        assert "citations" in q
