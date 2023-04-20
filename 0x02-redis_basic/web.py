#!/usr/bin/env python3
"""Web Module"""

from functools import wraps
import redis
import requests
from typing import Callable

_redis = redis.Redis()


def get_page(url: str) -> str:
    """Obtain the HTML content of a URL"""
    if _redis.get(f'count:{url}'):
        _redis.incr(f"count:{url}")
    else:
        _redis.set(f'count:{url}', 1)
    cached = _redis.get(f"cached:{url}")
    if cached:
        return cached.decode('utf-8')
    req = requests.get(url)
    html = req.text
    _redis.setex(f"cached:{url}", 10, html)
    return html
