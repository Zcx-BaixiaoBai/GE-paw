import os
root = 'src'

# paho
p = os.path.join(root, 'paho')
os.makedirs(os.path.join(p, 'mqtt'), exist_ok=True)
open(os.path.join(p, '__init__.py'), 'w', encoding='utf-8').write('')
open(os.path.join(p, 'mqtt', '__init__.py'), 'w', encoding='utf-8').write('')
open(os.path.join(p, 'mqtt', 'client.py'), 'w', encoding='utf-8').write('''"""Stub for paho.mqtt.client."""
from __future__ import annotations
from typing import Any, Callable, Optional


class _ReasonCodes:
    SUCCESS = 0


class MQTTv311:
    pass


class CallbackAPIVersion:
    VERSION1 = 'v1'
    VERSION2 = 'v2'


class MQTTMessage:
    def __init__(self) -> None:
        self.topic: str = ''
        self.payload: bytes = b''
        self.qos: int = 0
        self.retain: bool = False


class Client:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._on_connect: Optional[Callable] = None
        self._on_message: Optional[Callable] = None
        self._on_disconnect: Optional[Callable] = None
        self._on_subscribe: Optional[Callable] = None
        self._username: Optional[str] = kwargs.get('username')
        self._password: Optional[str] = kwargs.get('password')

    def username_pw_set(self, username=None, password=None) -> None:
        self._username = username
        self._password = password

    def connect(self, host: str, port: int = 1883, keepalive: int = 60) -> int:
        return 0

    def connect_async(self, host: str, port: int = 1883, keepalive: int = 60) -> int:
        return 0

    def disconnect(self) -> int:
        return 0

    def loop_start(self) -> None:
        return None

    def loop_stop(self) -> None:
        return None

    def loop_forever(self) -> int:
        return 0

    def publish(self, topic: str, payload=None, qos: int = 0, retain: bool = False) -> Any:
        class _Info:
            def __init__(self):
                self.rc = 0
                self.mid = 0
        return _Info()

    def subscribe(self, topic, qos: int = 0) -> Any:
        class _Info:
            def __init__(self):
                self.rc = 0
                self.mid = 0
        return _Info()

    def on_connect(self, client, userdata, flags, rc, *args) -> None:
        return None

    def on_message(self, client, userdata, msg) -> None:
        return None

    def on_disconnect(self, client, userdata, rc, *args) -> None:
        return None

    def on_subscribe(self, client, userdata, mid, granted_qos, *args) -> None:
        return None


reason_codes = _ReasonCodes
''')
open(os.path.join(p, 'mqtt', 'mqtt.py'), 'w', encoding='utf-8').write('''"""Stub for paho.mqtt.mqtt (alias)."""
from paho.mqtt.client import (
    Client,
    MQTTMessage,
    MQTTv311,
    CallbackAPIVersion,
    reason_codes,
)
''')


# segno
open(os.path.join(root, 'segno.py'), 'w', encoding='utf-8').write('''"""Stub for segno QR code library."""
from __future__ import annotations
from typing import Any


class _QRCode:
    def __init__(self, payload: str = '', **kwargs: Any) -> None:
        self.payload = payload
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self, target, **kwargs: Any) -> Any:
        if hasattr(target, 'write'):
            target.write(b'\\x89PNG\\r\\n\\x1a\\n')
            return None
        with open(target, 'wb') as fh:
            fh.write(b'\\x89PNG\\r\\n\\x1a\\n')
        return None

    def png_data(self, **kwargs: Any) -> bytes:
        return b'\\x89PNG\\r\\n\\x1a\\n'

    def svg_data(self, **kwargs: Any) -> bytes:
        return b'<svg/>'


def make(content: str, **kwargs: Any) -> _QRCode:
    return _QRCode(content, **kwargs)
''')


print('created paho/segno stubs')
