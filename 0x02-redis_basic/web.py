#!/usr/bin/env python3
"""Web Module"""

from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis()


def track_requests(method: Callable) -> Callable:
    """Decorator to track requests made to a url"""
    @wraps(method)
    def wrapper(url):
        """ Wrapper for decorator """
        redis_.incr(f"count:{url}")
        cached = redis_.get(f"cached:{url}")
        if cached:
            return cached.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@track_requests
def get_page(url: str) -> str:
    """Obtain the HTML content of a  URL"""
    req = requests.get(url)
    return req.text
