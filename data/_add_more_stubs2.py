import os
root = 'src'

# Add ChatbotHandler to dingtalk_stream
dp = os.path.join(root, 'dingtalk_stream', '__init__.py')
t = open(dp, encoding='utf-8').read()
if 'class ChatbotHandler' not in t:
    add = '''

class ChatbotHandler:
    """Stub for `dingtalk_stream.ChatbotHandler` base class."""

    def __init__(self) -> None:
        pass

    async def process(self, *args, **kwargs):
        return None

    def reply_text(self, *args, **kwargs):
        return None
'''
    open(dp, 'a', encoding='utf-8').write(add)
    print('ChatbotHandler added')

# Add google.protobuf.descriptor
gp = os.path.join(root, 'google', 'protobuf')
open(os.path.join(gp, 'descriptor.py'), 'w', encoding='utf-8').write('''"""Stub for google.protobuf.descriptor."""
from typing import Any


class FieldDescriptor:
    pass


class Descriptor:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def fields_by_name(self) -> dict:
        return {}


class FileDescriptor:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
''')
print('done')
