import sys
import redis
import uuid

from reqresp.reqresp import Queue

def work_handler(request_data):
    print("Got:", request_data)
    return {"data": "pong"}

def main(consumer_id):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    p = Queue(r, consumer_id, "pingpong")
    for i in xrange(5):
        p.process(work_handler)

if __name__ == "__main__":
    main(sys.argv[1])
