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

def count(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url, *args, **kwds):
        cache.incr(f"count:{url}")
        result = func(url, *args, **kwds)
        return result
    return wrapper

@count
def get_page(url: str) -> str:
    content = cache.get(url)

    if content:
        return content.decode("utf-8")
    else:
        response = requests.get(url)
        cache.setex(url, 10, response.text)
        return response.text


url = "http://slowwly.robertomurray.co.uk"
get_page(url)
print(cache.get(f"count:{url}"))
