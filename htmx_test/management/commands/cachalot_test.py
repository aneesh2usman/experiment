# automate_requests.py

from django.core.management.base import BaseCommand
import logging

from htmx_test.models import APIKey
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.core.cache import cache
def get_top_models(limit=10):

    """
    Get the top 10 models by name.
    """
    cached_data = cache.get('my_cached_data')
    
    if cached_data is not None:
        print("cached")
        return cached_data
    # If data is not in the cache, query the database
    data = APIKey.objects.all()  # Your database query here
    # Store the result in the cache
    cache.set('my_cached_data', data)

    return data

# @cache(60)  # Cache the result for 15 minutes
# def get_queryset_data():
#     print("***inside***")
#     return APIKey.objects.all()

from django.core.cache import cache

def set_cache(key, value, timeout=None):
    """
    Set the value of a cache entry.
    """
    cache.set(key, value, timeout)

def get_cache(key):
    """
    Get the value of a cache entry.
    """
    return cache.get(key)

def main():
    key = 'my_cache_key'
    value = 'my_cache_value'

    # set_cache('key1', 'value1')
    print(get_cache('key1'))  # value1
    set_cache('key2', 'value2')
    print(get_cache('key2')) 


    
class Command(BaseCommand):
    help = 'Automatically send requests to an external API'

    def handle(self, *args, **options):
        main()


