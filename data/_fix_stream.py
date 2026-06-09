from pathlib import Path
p = Path('src/gepaw/token_usage/model_wrapper.py')
t = p.read_text(encoding='utf-8')
old = '''

async def stream(self, *args, **kwargs):
    \"\"\"Stub stream to satisfy the abstract base.\"\"\"
    yield None

'''
new = ''
if old in t:
    t = t.replace(old, new, 1)
# Insert stream method inside the class
class_marker = 'class TokenRecordingModelWrapper(ChatModelBase):'
if class_marker in t and 'async def stream(' not in t.split('class TokenRecordingModelWrapper')[1].split('class')[0]:
    insert = '''

    async def stream(self, *args, **kwargs):
        \"\"\"Stub `stream` to satisfy the abstract base.\"\"\"
        yield None
'''
    # Insert right after the class declaration line
    t = t.replace(class_marker, class_marker + insert, 1)
p.write_text(t, encoding='utf-8')
print('fixed')
