from pathlib import Path
import re
files = [
    Path("src/gepaw/local_models/llamacpp.py"),
    Path("src/gepaw/local_models/model_manager.py"),
]
for f in files:
    data = f.read_bytes()
    new = data.replace(b"qwenpaw-llamacpp-download", b"gepaw-llamacpp-download")
    new = new.replace(b"qwenpaw-model-download", b"gepaw-model-download")
    print(f, "changed:", data != new)
    f.write_bytes(new)
