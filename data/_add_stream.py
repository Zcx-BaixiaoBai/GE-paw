from pathlib import Path
p = Path('src/gepaw/token_usage/model_wrapper.py')
t = p.read_text(encoding='utf-8')
if 'async def stream' not in t:
    add = '''

async def stream(self, *args, **kwargs):
    """Stub `stream` to satisfy the abstract base."""
    yield None
'''
    # Insert before the record_usage function
    marker = '\ndef record_usage('
    if marker in t:
        t = t.replace(marker, add + marker, 1)
    else:
        t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
