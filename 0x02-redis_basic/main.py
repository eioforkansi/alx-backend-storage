#!/usr/bin/env python3
"""
Main file
"""
from exercise import Cache

cache = Cache()

TEST_CASES = {
    b"foo": None,  # store and retrieve as bytes
    123: int,      # store and retrieve as integer
    "bar": lambda d: d.decode("utf-8")  # store as string, retrieve as string
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)  # Store the value in Redis
    assert cache.get(key, fn=fn) == value  # Assert that retrieved value is correct
