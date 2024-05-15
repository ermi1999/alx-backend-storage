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
        cached = r.get(f'result:{url}')
        if cached:
            return cached.decode('utf-8')
        res = fun(url)
        r.setex(f'result:{url}', 10, res)
        return res
    return wrapper


@cache_response
def get_page(url: str) -> str:
    """
    makes a reques to url.
    """
    return requests.get(url).text
