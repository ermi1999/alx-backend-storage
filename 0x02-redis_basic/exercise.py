#!/usr/bin/env python3
"""
module for writing into redis.
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional, Any


def call_history(method: Callable) -> Callable:
    """
    a decorator to store the history of a function call
    """
    @wraps(method)
    def wrapper(self: any, *args):
        """
        Wrapper
        """
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output
    return wrapper


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


def replay(fn: Callable) -> None:
    """
    displays the history of calls of a particular function.
    """
    r = redis.Redis()
    name = fn.__qualname__
    inputs = [i.decode('utf-8') for i in r.lrange(f'{name}:inputs', 0, -1)]
    outputs = [i.decode('utf-8') for i in r.lrange(f'{name}:outputs', 0, -1)]
    print(f"{fn.__qualname__} was called {r.get(name).decode('utf-8')} times:")
    for _input, output in zip(inputs, outputs):
        print(f"{name}(*{_input}) -> {output}")


class Cache:
    """
    class for writing into redis.
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
