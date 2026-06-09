"""Stub for paho.mqtt.client."""
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
