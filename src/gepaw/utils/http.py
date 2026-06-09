"""HTTP / loopback helpers for outbound requests.

Used by httpx wrappers and any place we need to decide whether to trust
environment proxy variables. Loopback targets (localhost / 127.0.0.0/8 /
::1) bypass the proxy by convention so local API calls do not leak via
HTTP_PROXY / HTTPS_PROXY.
"""
from __future__ import annotations

import ipaddress
from urllib.parse import urlparse

_LOOPBACK_HOST_NAMES = frozenset({"localhost"})


def is_loopback_host(host: str) -> bool:
    """Return True if ``host`` denotes the local machine.

    Accepts:
      - hostnames ``localhost`` (with optional trailing dot)
      - IPv4 / IPv6 literals whose ``is_loopback`` is True (127.0.0.0/8, ::1)
      - bracketed IPv6 literals like ``[::1]`` (brackets are stripped)
    """
    if not host:
        return False
    h = host.strip()
    if h.startswith("[") and h.endswith("]"):
        h = h[1:-1]
    if h.endswith("."):
        h = h[:-1]
    if h.lower() in _LOOPBACK_HOST_NAMES:
        return True
    try:
        return ipaddress.ip_address(h).is_loopback
    except ValueError:
        return False


def is_loopback_url(url: str) -> bool:
    """Return True if the URL's host is a loopback target."""
    if not url:
        return False
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    return is_loopback_host(parsed.hostname or "")


def trust_env_for_url(url: str) -> bool:
    """Decide whether httpx should honour environment proxy variables.

    Local / loopback URLs must always go direct so the local gepaw API
    is not accidentally routed through a corporate HTTP_PROXY.
    """
    return not is_loopback_url(url)