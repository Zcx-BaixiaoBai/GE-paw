from pathlib import Path
p = Path("tests/unit/gepaw/test_telegram_channel.py")
data = p.read_text()
if "import pytest" not in data and "pytest.mark.skip" in data:
    old = "from __future__ import annotations"
    new = "from __future__ import annotations\n\nimport pytest"
    data = data.replace(old, new, 1)
    p.write_text(data)
    print("added pytest import: test_telegram_channel.py")
