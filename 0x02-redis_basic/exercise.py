#!/usr/bin/env python3

"""
Module that provide Cache class
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def replay(method: Callable) -> None:
    """
    Function to display the history of calls of a particular function.
    """
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"
    inputs = redis.Redis().lrange(input_key, 0, -1)
    outputs = redis.Redis().lrange(output_key, 0, -1)
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        decoded_input = input.decode("utf-8")
        decoded_output = output.decode("utf-8")
        print(f"{method.__qualname__}(*{decoded_input}) -> {decoded_output}")


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs
    and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwds)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator that takes a single method Callable
    argument and returns a Callable.
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwds)
    return wrapper


class Cache:
    """
    Stores an instance of the Redis client as a private variable named
    _redis (using redis.Redis()) and flush the instance using flushdb.
    """
    def __init__(self):
        """
        Initializes a Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that takes a data argument and returns a string.
        The method generates a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """
        Method that take a key string argument and an optional
        Callable argument named fn. This callable will be used
        to convert the data back to the desired format.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage.
        """
        return self.get(key, fn=lambda data: data.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from a Redis data storage.
        """
        return self.get(key, lambda data: int(data))
