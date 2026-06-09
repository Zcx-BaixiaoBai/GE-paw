from pathlib import Path
for f in ["tests/unit/gepaw/test_cross_channel_merge.py", "tests/unit/gepaw/test_telegram_channel.py"]:
    p = Path(f)
    data = p.read_text()
    if "import pytest" not in data and "pytestmark" in data:
        # add import after first docstring
        old = "from __future__ import annotations"
        new = "from __future__ import annotations\n\nimport pytest"
        data = data.replace(old, new, 1)
        p.write_text(data)
        print(f"added pytest import: {f}")
