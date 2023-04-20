#!/usr/bin/env python3
"""Web Module"""

from functools import wraps
import redis
import requests

_redis = redis.Redis()


def get_page(url: str) -> str:
    """Obtain the HTML content of a URL"""
    print(_redis.get('count:{}'.format(url)))
    if not _redis.get('count:{}'.format(url)):
        _redis.set('count:{}'.format(url), 0)
    _redis.incr("count:{}".format(url))
    cached = _redis.get("cached:{}".format(url))
    if cached:
        return cached.decode('utf-8')
    req = requests.get(url)
    html = req.text
    _redis.setex("cached:{}".format(url), 10, html)
    return html
