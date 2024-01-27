#!/usr/bin/env python3
"""
 function & Module for Web
"""
import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    """ The wrapper function in decorator """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ The decorator to cache the result in time of 10 seconds """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        client.set(f'{url}', response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """ The function to get the URL from HTML """
    response = requests.get(url)
    return response.text
