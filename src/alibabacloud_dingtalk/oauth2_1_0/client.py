"""Stub for alibabacloud_dingtalk.oauth2_1_0.client."""
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
