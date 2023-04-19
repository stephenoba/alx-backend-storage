#!/usr/bin/env python3
"""
Module contains the Cache class
"""
import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts the number of times a method is called."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Store the history of inputs and outputs for a particular function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """"""
    method_name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(method_name).decode("utf-8")
    print("{} was called {} times:".format(method_name, calls))
    inputs = cache.lrange(method_name + ":inputs", 0, -1)
    outputs = cache.lrange(method_name + ":outputs", 0, -1)
    for _in, _out in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            method_name, _in.decode('utf-8'),
            _out.decode('utf-8')))


class Cache:
    """
    Mapping for cache object. manages data using Redis
    """
    def __init__(self):
        """
        Initialize a Cache object
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generate a random key, and store the input data in
        Redis using the random key

        Args
        ----
        data (Any): Data to be stoed in the Cache

        Returns
        -------
        A key(str) for the data stored
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Get a value from cache

        Args
        ----
        key (str): Key used in fetching value
        fn: callable used to convert the data back to the desired format

        Returns
        -------
        The data
        """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Get a string from the cache."""
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """Get an int from the cache."""
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
