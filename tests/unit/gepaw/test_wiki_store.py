"""Unit tests for WikiStore sandbox (raw/graph must be rejected, .. must be rejected)."""
from __future__ import annotations

import os
import shutil
import tempfile
import pytest

from gepaw.wiki.store import FilesystemWikiStore, _safe_rel
from gepaw.models.wiki import WikiCorpus


@pytest.fixture
def store():
    tmp = tempfile.mkdtemp(prefix="gepaw-test-")
    corpus = WikiCorpus(id="c1", org_id="o1", name="default", root_path=tmp, storage_kind="fs")
    s = FilesystemWikiStore(corpus)
    # seed a wiki file
    s.write_text("wiki/index.md", "# Index\nhello")
    s.write_text("wiki/overview.md", "# Overview\nworld")
    yield s
    shutil.rmtree(tmp, ignore_errors=True)


def test_safe_rel_accepts_wiki_subpath(store):
    assert _safe_rel("wiki") == "wiki"
    assert _safe_rel("wiki/index.md") == "wiki/index.md"
    assert _safe_rel("wiki/") == "wiki"


def test_safe_rel_rejects_traversal(store):
    with pytest.raises(PermissionError):
        _safe_rel("../etc/passwd")
    with pytest.raises(PermissionError):
        _safe_rel("wiki/../../escape")


def test_safe_rel_rewrites_absolute_to_wiki(store):
    # bare path with no wiki prefix is forced into wiki/
    with pytest.raises(PermissionError):
        _safe_rel("foo.md")
