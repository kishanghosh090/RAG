from redis import Redis
from rq import Queue

queue = Queue(
    connection = Redis(
        host="13.204.134.210",
        port="6379"
    )
)
# queue.enqueue()