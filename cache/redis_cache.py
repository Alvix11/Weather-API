import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def view_cached():
    """Prints all keys and values stored in Redis."""
    for key in redis_client.keys():
        value = redis_client.get(key)
        print(key.decode(errors="replace"), value.decode(errors="replace"))

def delete_cached():
    """Deletes all Redis cache (use with caution!)."""
    redis_client.flushdb()

def delete_key(key):
    """Deletes a specific key from the cache."""
    redis_client.delete(key)