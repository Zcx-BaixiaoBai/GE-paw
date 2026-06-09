from pathlib import Path
p = Path("src/gepaw/app/channels/qq/channel.py")
data = p.read_bytes()
old = b'''    return (
        "304003" in payload_text
        or "40034028" in payload_text
        or "\xe4\xb8\x8d\xe5\x85\x81\xe8\xae\xb8\xe5\x8c\x85\xe5\x90\xaburl" in payload_text
        or "url" in payload_text
    )\r
        return value.strip().lower() in {"1", "true", "yes", "on"}\r
    return bool(value)'''
new = b'''    return (
        "304003" in payload_text
        or "40034028" in payload_text
        or "\xe4\xb8\x8d\xe5\x85\x81\xe8\xae\xb8\xe5\x8c\x85\xe5\x90\xaburl" in payload_text
        or "url" in payload_text
    )


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)'''
print("found:", old in data)
data = data.replace(old, new)
p.write_bytes(data)
print("done")
