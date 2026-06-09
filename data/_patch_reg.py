from pathlib import Path
p = Path("src/gepaw/app/channels/registry.py")
data = p.read_bytes()
old = b"\r\n\r\nCHANNEL_KINDS = (\r\n"
new = b'''\r\n\r\ndef get_adapter_class(kind):\r\n    """Return the adapter class for ``kind`` (built-in or registered custom)."""\r\n    if not kind:\r\n        return None\r\n    return get_channel_registry().get(kind)\r\n\r\n\r\ndef build_adapter(\r\n    kind,\r\n    *,\r\n    account_id,\r\n    org_id,\r\n    name,\r\n    config=None,\r\n):\r\n    """Instantiate an adapter for ``kind``.\r\n\r\n    Unknown kinds fall back to the echo adapter so the rest of the\r\n    pipeline still has something usable to talk to.\r\n    """\r\n    cls = get_adapter_class(kind)\r\n    if cls is None:\r\n        from .kinds.echo import EchoAdapter\r\n        cls = EchoAdapter\r\n    return cls(\r\n        account_id=account_id,\r\n        org_id=org_id,\r\n        name=name,\r\n        config=config or {},\r\n    )\r\n\r\n\r\nCHANNEL_KINDS = (\r\n'''
print("found:", old in data)
data = data.replace(old, new)
p.write_bytes(data)
print("done")
