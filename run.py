import redis

from reqresp.reqresp import Queue

def main():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    p = Queue(r, "producer1", "pingpong", producer=True)
    resps = p.request({"data": "ping"})

    print("Got the following responses", resps)

if __name__ == "__main__":
    main()
