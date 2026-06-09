from pathlib import Path
p = Path('src/agentscope_runtime/engine/schemas/agent_schemas.py')
t = p.read_text(encoding='utf-8')
# Add REFUSAL to ContentType
t = t.replace('DATA = "data"', 'DATA = "data"\n    REFUSAL = "refusal"')
# Add channel_meta to AgentRequest
old = '''class AgentRequest(BaseModel):
    """Inbound agent request, used by channel adapters."""

    session_id: str = Field(default="")
    user_id: str = Field(default="")
    channel: str = Field(default="")
    sender_id: Optional[str] = Field(default=None)
    content_parts: List[Any] = Field(default_factory=list)
    text: str = Field(default="")
    metadata: dict = Field(default_factory=dict)
    raw: Any = Field(default=None)'''
new = '''class AgentRequest(BaseModel):
    """Inbound agent request, used by channel adapters."""

    model_config = {"extra": "allow"}
    session_id: str = Field(default="")
    user_id: str = Field(default="")
    channel: str = Field(default="")
    sender_id: Optional[str] = Field(default=None)
    content_parts: List[Any] = Field(default_factory=list)
    text: str = Field(default="")
    metadata: dict = Field(default_factory=dict)
    raw: Any = Field(default=None)
    channel_meta: Optional[Any] = Field(default=None)
    input: List[Any] = Field(default_factory=list)'''
if old in t:
    t = t.replace(old, new, 1)
    p.write_text(t, encoding='utf-8')
    print('updated AgentRequest')
else:
    print('AgentRequest block not found, trying simpler change')
    if 'channel_meta' not in t:
        t = t + '''

# Extended AgentRequest (allow extra fields)
AgentRequest.model_config = getattr(AgentRequest, 'model_config', {}) or {}
if isinstance(AgentRequest.model_config, dict):
    AgentRequest.model_config['extra'] = 'allow'
'''
        p.write_text(t, encoding='utf-8')
        print('appended config tweak')
