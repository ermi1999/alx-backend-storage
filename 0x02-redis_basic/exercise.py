#!/usr/bin/env python3
"""
module for writing into redis.
"""
import redis
import uuid


class Cache:
    """
    class for writing into redis.
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    def store(self, data: str | bytes | int | float) -> str:
        """
        stores a data.
        """
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key