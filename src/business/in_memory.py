import redis
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0)
