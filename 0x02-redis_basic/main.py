#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache
replay = __import__('exercise').replay

# Test the implementation
cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)

# Call the replay function to display history
replay(cache.store)
