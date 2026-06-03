"""Small cache-backed rate limiting helpers for abuse-prone form endpoints."""

from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from django.core.cache import cache


@dataclass(frozen=True)
class RateLimitResult:
    limited: bool
    count: int
    limit: int
    window: int


def parse_rate(value: str) -> tuple[int, int]:
    """Parse a configurable rate value in ``requests/window_seconds`` format."""
    amount, window = value.split("/", 1)
    return int(amount), int(window)


def client_identifier(request) -> str:
    """Build a privacy-conscious identifier from user id or client IP."""
    if request.user.is_authenticated:
        return f"user:{request.user.pk}"
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    ip_address = forwarded_for.split(",")[0].strip() if forwarded_for else request.META.get("REMOTE_ADDR", "unknown")
    return f"ip:{ip_address}"


def check_rate_limit(request, scope: str) -> RateLimitResult:
    """Increment and check the configured rate limit for a scope."""
    limit, window = parse_rate(settings.RATE_LIMITS[scope])
    key = f"rate-limit:{scope}:{client_identifier(request)}"
    added = cache.add(key, 1, timeout=window)
    if added:
        count = 1
    else:
        try:
            count = cache.incr(key)
        except ValueError:
            cache.set(key, 1, timeout=window)
            count = 1
    return RateLimitResult(limited=count > limit, count=count, limit=limit, window=window)
