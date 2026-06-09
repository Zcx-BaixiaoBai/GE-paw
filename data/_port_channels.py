import subprocess
import os

# Get list of all files in qwenpaw/app/channels
result = subprocess.check_output(
    ["git", "-c", "core.quotepath=false", "ls-tree", "-r", "--name-only",
     "16688432fbc0a0e7a65baa309bf83318b7ed79f0"]
).decode("utf-8")
files = [f for f in result.split("\n") if f.startswith("src/qwenpaw/app/channels/") and f.endswith(".py")]

for src in files:
    dst = src.replace("qwenpaw", "gepaw")
    raw = subprocess.check_output(
        ["git", "-c", "core.quotepath=false", "show",
         "16688432fbc0a0e7a65baa309bf83318b7ed79f0:" + src]
    )
    text = raw.decode("utf-8").replace("qwenpaw", "gepaw")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
print("wrote", len(files), "files")