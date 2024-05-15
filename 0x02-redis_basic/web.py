#!/usr/bin/env python3
"""
module for requesting a page.
"""
import requests
import redis
from functools import wraps
from typing import Callable


def cache_response(fun: Callable) -> Callable:
    """
    A decorator for caching a response and for counting a request. 
    """
    @wraps(fun)
    def wrapper(url: str) -> str:
        r = redis.Redis()
        r.incr(f'count:{url}')
        cached = r.get(f'{url}')
        if cached:
            return cached.decode('utf-8')
        res = fun(url)
        r.set(url, res, 10)
        return res
    return wrapper

@cache_response
def get_page(url: str) -> str:
    """
    makes a reques to url.
    """
    res = requests.get(url)
    return res.text