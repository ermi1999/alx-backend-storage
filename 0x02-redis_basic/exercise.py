#!/usr/bin/env python3
"""
module for writing into redis.
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional, Any


def count_calls(method: Callable) -> Callable:
    """
    a decorator function to count how many times
    a function gets called.
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs):
        """
        wrapper function.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    class for writing into redis.
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """
        stores a data.
        """
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> any:
        """
        gets a value from a redis database
        converts it to correct type and returns it.
        """
        value = self._redis.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, value: bytes) -> str:
        """Converts a byte to string"""
        return value.decode('utf-8')

    def get_int(self, value: bytes) -> int:
        """Converts a byte to int"""
        return int(value)
