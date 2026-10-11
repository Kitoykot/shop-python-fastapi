from rq import Queue

from config.queue.connection import queue


def get_queue() -> Queue:
    return queue
