from pathlib import Path
p = Path('src/gepaw/token_usage/model_wrapper.py')
t = p.read_text(encoding='utf-8')
if 'def record_usage(' not in t:
    add = '''

def record_usage(
    provider_id: str,
    model_name: str,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    cache_read_tokens: int = 0,
    cache_write_tokens: int = 0,
    cost_cents: float = 0.0,
    session_id: str = '',
    user_id: str = '',
    agent_id: str = '',
    raw: dict = None,
) -> None:
    """Convenience wrapper to record a usage event via the manager."""
    from .manager import get_token_usage_manager

    manager = get_token_usage_manager()
    manager.enqueue(
        provider_id=provider_id,
        model_name=model_name,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cache_read_tokens=cache_read_tokens,
        cache_write_tokens=cache_write_tokens,
        cost_cents=cost_cents,
        session_id=session_id,
        user_id=user_id,
        agent_id=agent_id,
        raw=raw or {},
    )
'''
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
