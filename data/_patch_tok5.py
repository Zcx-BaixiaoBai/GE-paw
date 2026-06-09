from pathlib import Path
p = Path("src/gepaw/token_usage/model_wrapper.py")
data = p.read_bytes()
old = b'''def record_usage(\r\n    db = None,\r\n    *,\r\n    org_id: str = "",\r\n    model: str = "",\r\n    provider_id: str = "",\r\n    model_name: str = "",\r\n    prompt_tokens: int = 0,\r\n    completion_tokens: int = 0,\r\n    cache_read_tokens: int = 0,\r\n    cache_write_tokens: int = 0,\r\n    cost_cents: float = 0.0,\r\n    session_id = "",\r\n    user_id = None,\r\n    agent_id: str = "",\r\n    raw: dict = None,\r\n) -> int:'''
new = b'''def record_usage(\r\n    db = None,\r\n    *,\r\n    org_id: str = "",\r\n    model: str = "",\r\n    provider_id: str = "",\r\n    model_name: str = "",\r\n    prompt_tokens: int = 0,\r\n    completion_tokens: int = 0,\r\n    cache_read_tokens: int = 0,\r\n    cache_write_tokens: int = 0,\r\n    cost_cents: float = 0.0,\r\n    session_id = "",\r\n    user_id = None,\r\n    agent_id: str = "",\r\n    raw: dict = None,\r\n    commit: bool = True,\r\n) -> int:'''
print("found:", old in data)
data = data.replace(old, new)
# Add commit handling in DB block
old2 = b'''        # Filter to columns the table actually has.\r\n        valid = {k: v for k, v in kwargs.items() if k in TokenUsageLog.__table__.columns}\r\n        row = TokenUsageLog(**valid)'''
new2 = b'''        # Filter to columns the table actually has.\r\n        valid = {k: v for k, v in kwargs.items() if k in TokenUsageLog.__table__.columns}\r\n        row = TokenUsageLog(**valid)\r\n        db.add(row)\r\n        if commit:\r\n            try:\r\n                db.flush()\r\n            except Exception:\r\n                pass'''
# Remove the existing db.add(row) since it duplicates
old3 = b'''        db.add(row)\r\n        try:\r\n            db.flush()\r\n        except Exception:\r\n            pass\r\n        return getattr(row, "id", 0) or 0'''
new3 = b'''        return getattr(row, "id", 0) or 0'''
print("found2:", old2 in data, "found3:", old3 in data)
data = data.replace(old2, new2)
data = data.replace(old3, new3)
p.write_bytes(data)
print("done")
