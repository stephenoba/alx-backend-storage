#!/usr/bin/env python3
"""
Module contains the Cache class
"""
import uuid
import redis
from typing import Union


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

    def store(self, data: Union[int, str, bytes, float]) -> str:
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
        self._redis.set({key: data})
        return key
