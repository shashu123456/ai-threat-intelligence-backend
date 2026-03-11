import redis
from rq import Queue

redis_conn = redis.Redis()

queue = Queue(connection=redis_conn)