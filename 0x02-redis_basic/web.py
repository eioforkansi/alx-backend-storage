#!/usr/bin/env python3

"""
Module with the implementation of get_page which
uses the request module to obtain the HTML content
of a particular URL and returns it.  
"""

import requests
import redis
from typing import Callable
from functools import wraps

cache = redis.Redis()

def cache_page(func):
    @wraps(func)
    def wrapper(url: str) -> str:
        # Track access count
        cache_key_count = f"count:{url}"
        cache.incr(cache_key_count)

        # Cache key for storing the page content
        cache_key_content = f"content:{url}"
        cached_content = cache.get(cache_key_content)

        # Return cached content if available
        if cached_content:
            return cached_content.decode('utf-8')

        # Call the original function and cache the result
        content = func(url)
        cache.setex(cache_key_content, 10, content)

        return content
    return wrapper

@cache_page
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
