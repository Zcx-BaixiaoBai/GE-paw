from pathlib import Path
p = Path('src/gepaw/app/channels/base.py')
t = p.read_text(encoding='utf-8')
if 'IncomingMessage' not in t:
    t = t + '''

class IncomingMessage:
    \"\"\"Stub `IncomingMessage` channel payload.\"\"\"

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
'''
    p.write_text(t, encoding='utf-8')
    print('added')
