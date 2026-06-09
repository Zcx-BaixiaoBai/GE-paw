"""Stub for alibabacloud_dingtalk.card_1_0.models."""
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


class GetAccessTokenRequest:
    """Stub model GetAccessTokenRequest."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class GetAccessTokenResponse:
    """Stub model GetAccessTokenResponse."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class GetAccessTokenResponseBody:
    """Stub model GetAccessTokenResponseBody."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class DeliverCardRequest:
    """Stub model DeliverCardRequest."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class DeliverCardRequestImGroupOpenDeliverModel:
    """Stub model DeliverCardRequestImGroupOpenDeliverModel."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class DeliverCardRequestImRobotOpenDeliverModel:
    """Stub model DeliverCardRequestImRobotOpenDeliverModel."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class DeliverCardResponse:
    """Stub model DeliverCardResponse."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class DeliverCardResponseBody:
    """Stub model DeliverCardResponseBody."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class UpdateCardInstanceRequest:
    """Stub model UpdateCardInstanceRequest."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class UpdateCardInstanceRequestCardData:
    """Stub model UpdateCardInstanceRequestCardData."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class UpdateCardInstanceResponse:
    """Stub model UpdateCardInstanceResponse."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class OauthAccessTokenRequest:
    """Stub model OauthAccessTokenRequest."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class OauthAccessTokenResponse:
    """Stub model OauthAccessTokenResponse."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class OauthRefreshTokenRequest:
    """Stub model OauthRefreshTokenRequest."""

    def __init__(self, *args, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
