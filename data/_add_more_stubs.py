import os
root = 'src'

# Add CallbackMessage to dingtalk_stream
dp = os.path.join(root, 'dingtalk_stream', '__init__.py')
t = open(dp, encoding='utf-8').read()
if 'class CallbackMessage' not in t:
    add = '''

class CallbackMessage:
    """Stub for `dingtalk_stream.CallbackMessage`."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_dict(cls, data):
        return cls(**(data or {}))
'''
    t = t + add
    open(dp, 'w', encoding='utf-8').write(t)
    print('CallbackMessage added')

# Add CallbackHandler
if 'class CallbackHandler' not in t:
    add2 = '''

class CallbackHandler:
    """Stub for `dingtalk_stream.CallbackHandler`."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
'''
    open(dp, 'a', encoding='utf-8').write(add2)
    print('CallbackHandler added')

# Add MQTTException to paho.mqtt
mp = os.path.join(root, 'paho', 'mqtt', '__init__.py')
mt = open(mp, encoding='utf-8').read()
if 'MQTTException' not in mt:
    open(mp, 'a', encoding='utf-8').write('''

class MQTTException(Exception):
    '''+ '"""Stub for `paho.mqtt.MQTTException`."""' + '''
''')
    print('MQTTException added to paho.mqtt')

# Add mqtt.py alias for paho.mqtt.mqtt
open(os.path.join(root, 'paho', 'mqtt', 'mqtt.py'), 'w', encoding='utf-8').write('''"""Alias module for paho.mqtt.mqtt."""
from paho.mqtt.client import (
    Client,
    MQTTMessage,
    MQTTv311,
    CallbackAPIVersion,
    reason_codes,
)
from paho.mqtt import MQTTException
''')

# Create google.protobuf stub
gp = os.path.join(root, 'google')
os.makedirs(gp, exist_ok=True)
open(os.path.join(gp, '__init__.py'), 'w', encoding='utf-8').write('')
op = os.path.join(gp, 'protobuf')
os.makedirs(op, exist_ok=True)
open(os.path.join(op, '__init__.py'), 'w', encoding='utf-8').write('')
open(os.path.join(op, 'descriptor_pb2.py'), 'w', encoding='utf-8').write('''"""Stub for google.protobuf.descriptor_pb2."""
''')
open(os.path.join(op, 'descriptor_pool.py'), 'w', encoding='utf-8').write('''"""Stub for google.protobuf.descriptor_pool."""
from typing import Any


class DescriptorPool:
    def __init__(self) -> None:
        pass

    def FindMessageTypeByName(self, name: str) -> Any:
        return None

    def Add(self, file_desc) -> None:
        return None


_default = DescriptorPool()


def Default() -> DescriptorPool:
    return _default
''')
open(os.path.join(op, 'json_format.py'), 'w', encoding='utf-8').write('''"""Stub for google.protobuf.json_format."""
from typing import Any


def Parse(text: str, message: Any) -> Any:
    return message


def MessageToDict(message: Any) -> dict:
    return {}


def MessageToJson(message: Any) -> str:
    return '{}'


def ParseDict(js_dict: dict, message: Any) -> Any:
    return message
''')

print('done')
