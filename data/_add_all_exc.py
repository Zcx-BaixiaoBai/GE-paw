from pathlib import Path
p = Path('src/agentscope_runtime/engine/schemas/exception.py')
t = p.read_text(encoding='utf-8')
extras = [
    'ModelQuotaExceededException',
    'UnauthorizedModelAccessException',
    'ModelExecutionException',
    'ModelTimeoutException',
    'RateLimitExceededException',
    'ModelContextLengthExceededException',
    'ExternalServiceException',
    'UnknownAgentException',
]
adds = []
for e in extras:
    if e not in t:
        adds.append(f'''

class {e}(AgentException):
    pass
''')
if adds:
    t = t + ''.join(adds)
    p.write_text(t, encoding='utf-8')
    print('added', len(adds))
