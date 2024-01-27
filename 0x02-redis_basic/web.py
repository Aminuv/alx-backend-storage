#!/usr/bin/env python3
"""
    function & Module for Web
"""
import requests
import redis
from functools import wraps

r = redis.Redis()


def count_url_calls(func):
    """ The decorator to count """
    @wraps(func)
    def wrapper(url):
        """ The wrapper function in decorator """
        r.incr(f"count:{url}")
        return func(url)
    return wrapper

def cache_page(func):
    """ The decorator to cache the result in time of 10 seconds """
    @wraps(func)
    def wrapper(url):
        """ The function for the decorator """
        result = r.get(url)
        if result is None:
            result = func(url)
            r.set(url, result, ex=10)
        return result
    return wrapper

@count_url_calls
@cache_page
def get_page(url: str) -> str:
    """ The function to get the URL from HTML """
    response = requests.get(url)
    return response.text
