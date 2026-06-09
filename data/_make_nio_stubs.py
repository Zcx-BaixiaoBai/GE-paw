import os
base = 'src/nio'
os.makedirs(os.path.join(base, 'event_builders'), exist_ok=True)
os.makedirs(os.path.join(base, 'events'), exist_ok=True)
os.makedirs(os.path.join(base, 'crypto'), exist_ok=True)

# nio/responses.py
open(os.path.join(base, 'responses.py'), 'w', encoding='utf-8').write('''"""Stub for nio.responses."""
from __future__ import annotations
from typing import Any


class _BaseResponse:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{type(self).__name__}({attrs})'


class WhoamiResponse(_BaseResponse):
    pass


class JoinedMembersResponse(_BaseResponse):
    pass


class RoomGetStateEventResponse(_BaseResponse):
    pass


class SyncError(Exception):
    """Stub for nio.responses.SyncError."""

    def __init__(self, message: str = '', *args, **kwargs) -> None:
        super().__init__(message)
        self.message = message
        for k, v in kwargs.items():
            setattr(self, k, v)
''')

# nio/event_builders/direct_messages.py
open(os.path.join(base, 'event_builders', 'direct_messages.py'), 'w', encoding='utf-8').write('''"""Stub for nio.event_builders.direct_messages."""
from __future__ import annotations
from typing import Any


class ToDeviceMessage:
    """Stub `nio.event_builders.direct_messages.ToDeviceMessage`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_dict(self) -> dict:
        return dict(self.__dict__)
''')

# nio/events/to_device.py
open(os.path.join(base, 'events', '__init__.py'), 'w', encoding='utf-8').write('')
open(os.path.join(base, 'events', 'to_device.py'), 'w', encoding='utf-8').write('''"""Stub for nio.events.to_device."""
from __future__ import annotations
from typing import Any


class _ToDeviceBase:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class RoomKeyRequest(_ToDeviceBase):
    pass


class RoomKeyRequestCancellation(_ToDeviceBase):
    pass
''')

# nio/crypto/attachments.py
open(os.path.join(base, 'crypto', '__init__.py'), 'w', encoding='utf-8').write('')
open(os.path.join(base, 'crypto', 'attachments.py'), 'w', encoding='utf-8').write('''"""Stub for nio.crypto.attachments."""
from __future__ import annotations
from typing import Any, Optional


def decrypt_attachment(ciphertext: bytes, key: Any, hash_str: str) -> bytes:
    """Return the ciphertext as-is (stub)."""
    return ciphertext


def encrypt_attachment(plaintext: bytes, key: Any = None) -> tuple[bytes, str, str]:
    """Return (plaintext, '', '') (stub)."""
    return plaintext, '', ''
''')

print('created nio stubs')
