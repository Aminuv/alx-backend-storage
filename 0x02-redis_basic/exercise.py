#!/usr/bin/env python3
""" § Module for Cache """

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ the Decorator to count how many times methods"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ the  Decorator to store the history of inputs """
    inkey = method.__qualname__ + ":inputs"
    outkey = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ function for the decorator """
        self._redis.rpush(inkey, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(outkey, str(res))
        return res

    return wrapper


def replay(method: Callable) -> None:
    """ the Function to display the history """
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )


class Cache:
    """ the Cache class """

    def __init__(self):
        """ doc Initialize"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ doc Store the input data """
        keyx = str(uuid.uuid4())
        self._redis.set(keyx, data)
        return keyx

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """ doc Get the value of a key """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ doc the value of a key """
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """ the value of a key and convert it to an integer """
        return self.get(key, fn=int)
