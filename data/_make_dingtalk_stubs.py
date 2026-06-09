import os
root = 'src'

# dingtalk_stream
p = os.path.join(root, 'dingtalk_stream')
os.makedirs(p, exist_ok=True)
open(os.path.join(p, '__init__.py'), 'w', encoding='utf-8').write('''"""Stub for dingtalk_stream SDK."""
from __future__ import annotations
from typing import Any


class ChatbotMessage:
    """Stub for `dingtalk_stream.ChatbotMessage`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_dict(cls, data: dict) -> "ChatbotMessage":
        return cls(**(data or {}))

    def to_dict(self) -> dict:
        return dict(self.__dict__)


class Credential:
    """Stub for `dingtalk_stream.Credential`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class DingTalkStreamClient:
    """Stub for `dingtalk_stream.DingTalkStreamClient`."""

    def __init__(self, credential: Any = None) -> None:
        self.credential = credential

    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None

    def register_callback_handler(self, *args: Any, **kwargs: Any) -> None:
        return None
''')

# alibabacloud_tea_openapi
p = os.path.join(root, 'alibabacloud_tea_openapi')
os.makedirs(p, exist_ok=True)
open(os.path.join(p, '__init__.py'), 'w', encoding='utf-8').write('''"""Stub for alibabacloud_tea_openapi."""
''')
open(os.path.join(p, 'models.py'), 'w', encoding='utf-8').write('''"""Stub models for alibabacloud_tea_openapi."""
from __future__ import annotations
from typing import Any


class Config:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class RuntimeOptions:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class Credential:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
''')

# alibabacloud_tea_util
p = os.path.join(root, 'alibabacloud_tea_util')
os.makedirs(p, exist_ok=True)
open(os.path.join(p, '__init__.py'), 'w', encoding='utf-8').write('')
open(os.path.join(p, 'models.py'), 'w', encoding='utf-8').write('''"""Stub models for alibabacloud_tea_util."""
from __future__ import annotations
from typing import Any


class RuntimeOptions:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
''')

# Tea
p = os.path.join(root, 'Tea')
os.makedirs(os.path.join(p, 'exceptions'), exist_ok=True)
open(os.path.join(p, '__init__.py'), 'w', encoding='utf-8').write('')
open(os.path.join(p, 'exceptions', '__init__.py'), 'w', encoding='utf-8').write('''"""Stub for Tea.exceptions."""
from __future__ import annotations


class TeaException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        self.code = kwargs.get("code", "")
        self.message = kwargs.get("message", "")
        self.data = kwargs.get("data", None)
        self.stack_trace = kwargs.get("stackTrace", "")
''')

# alibabacloud_dingtalk
p = os.path.join(root, 'alibabacloud_dingtalk')
os.makedirs(p, exist_ok=True)
open(os.path.join(p, '__init__.py'), 'w', encoding='utf-8').write('')

for pkg, classes in [
    ('oauth2_1_0', ['client', 'models']),
    ('robot_1_0', ['client', 'models']),
    ('card_1_0', ['client', 'models']),
]:
    sub = os.path.join(p, pkg)
    os.makedirs(sub, exist_ok=True)
    open(os.path.join(sub, '__init__.py'), 'w', encoding='utf-8').write('')
    for c in classes:
        open(os.path.join(sub, c + '.py'), 'w', encoding='utf-8').write('''"""Stub for alibabacloud_dingtalk.{pkg}.{c}."""
from __future__ import annotations
from typing import Any


class _Model:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class Client:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._config = kwargs.get("config")

    async def do_rpc_request(self, *args: Any, **kwargs: Any) -> Any:
        return _Model()

    async def do_request(self, *args: Any, **kwargs: Any) -> Any:
        return _Model()

    async def get_access_token(self, *args: Any, **kwargs: Any) -> Any:
        return _Model(access_token="stub", expire_time=7200)

    async def create_card_instance(self, *args: Any, **kwargs: Any) -> Any:
        return _Model()

    async def update_card_instance(self, *args: Any, **kwargs: Any) -> Any:
        return _Model()
'''.replace('{pkg}', pkg).replace('{c}', c))

# Add a few common model classes the test/client expects
for pkg in ('oauth2_1_0', 'robot_1_0', 'card_1_0'):
    sub = os.path.join(p, pkg)
    # Append common class names so attribute lookups succeed
    with open(os.path.join(sub, 'models.py'), 'a', encoding='utf-8') as fh:
        for cls_name in (
            'GetAccessTokenRequest',
            'GetAccessTokenResponse',
            'GetAccessTokenResponseBody',
            'DeliverCardRequest',
            'DeliverCardRequestImGroupOpenDeliverModel',
            'DeliverCardRequestImRobotOpenDeliverModel',
            'DeliverCardResponse',
            'DeliverCardResponseBody',
            'UpdateCardInstanceRequest',
            'UpdateCardInstanceRequestCardData',
            'UpdateCardInstanceResponse',
            'OauthAccessTokenRequest',
            'OauthAccessTokenResponse',
            'OauthRefreshTokenRequest',
        ):
            fh.write(f'''

class {cls_name}:
    """Stub model {cls_name}."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
''')

print('created dingtalk stubs')
