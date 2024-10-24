#!/usr/bin/env python3

"""
Module that provide Cache class
"""

import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """
        Stores an instance of the Redis client as a private variable
        named _redis (using redis.Redis())
        and flush the instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that takes a data argument and returns a string.
        The method generates a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.
        """
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key
