from pathlib import Path
p = Path("src/gepaw/app/channels/qq/channel.py")
data = p.read_bytes()
idx = data.find(b"    return (")
chunk = data[idx:idx+250]
for line in chunk.split(b"\n")[:10]:
    print("LINE:", repr(line))
