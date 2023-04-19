#!/usr/bin/env python3
"""
Module contains the Cache class
"""
import uuid
import redis
from typing import Union, Callable, Optional


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
