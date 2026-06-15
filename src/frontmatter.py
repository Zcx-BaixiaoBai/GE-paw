"""Stub for python-frontmatter."""
from typing import Any, Dict, Optional


def loads(text: str, **kwargs) -> 'Post':
    if text.startswith('---'):
        # crude YAML frontmatter parser
        body_start = text.find('---', 3)
        if body_start > 0:
            fm = text[3:body_start].strip()
            body = text[body_start+3:].lstrip(chr(10))
            metadata: Dict[str, Any] = {}
            for line in fm.splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    metadata[k.strip()] = v.strip()
            return Post(body, **metadata)
    return Post(text)


def load(fd, **kwargs) -> 'Post':
    if hasattr(fd, 'read'):
        text = fd.read()
    else:
        with open(fd, encoding='utf-8') as f:
            text = f.read()
    return loads(text, **kwargs)


def dumps(post: 'Post', **kwargs) -> str:
    fm_lines = ['---']
    for k, v in post.metadata.items():
        fm_lines.append(f'{k}: {v}')
    fm_lines.append('---')
    return chr(10).join(fm_lines) + chr(10) + post.content


class Post:
    def __init__(self, content: str = '', **metadata: Any) -> None:
        self.content = content
        self.metadata = dict(metadata)

    def __getitem__(self, key: str) -> Any:
        return self.metadata.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def keys(self):
        return self.metadata.keys()

    def values(self):
        return self.metadata.values()

    def items(self):
        return self.metadata.items()
