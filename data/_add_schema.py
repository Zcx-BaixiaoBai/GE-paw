from pathlib import Path
p = Path('src/acp/schema.py')
t = p.read_text(encoding='utf-8')
classes = [
    'AgentCapabilities', 'AgentMessageChunk', 'AgentPlanUpdate', 'AgentThoughtChunk',
    'AudioContentBlock', 'AvailableCommandsUpdate', 'ClientCapabilities',
    'CloseSessionResponse', 'CurrentModeUpdate', 'EmbeddedResourceContentBlock',
    'HttpMcpServer', 'ImageContentBlock', 'Implementation', 'ListSessionsResponse',
    'McpServerStdio', 'RequestPermissionResponse', 'ResourceContentBlock',
    'ResumeSessionResponse', 'SessionCapabilities', 'SessionCloseCapabilities',
    'SessionConfigOptionSelect', 'SessionConfigSelectOption', 'SessionInfo',
    'SessionListCapabilities', 'SessionResumeCapabilities',
    'SetSessionConfigOptionResponse', 'SseMcpServer', 'TextContentBlock',
    'UserMessageChunk',
]
add = chr(10).join([f'''

class {c}:
    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
''' for c in classes if c not in t])
if add.strip():
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added', len(classes))
else:
    print('exists')
