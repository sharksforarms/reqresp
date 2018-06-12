import uuid
import redis
import polling

class KeyPattern(object):
    @staticmethod
    def consumers(topic):
        return "{}:consumers".format(topic)
    @staticmethod
    def consumer(topic, consumer_id):
        return "{}:consumer:{}".format(topic, consumer_id)
    @staticmethod
    def request(topic, request_id):
        return "{}:request:{}".format(topic, request_id)
    @staticmethod
    def response(topic, consumer_id, request_id):
        return "{}:response:{}:{}".format(topic, request_id, consumer_id)

class Queue(object):
    def __init__(self, redis_con, consumer_id, topic, producer=False):
        self.consumer_id = consumer_id
        self.topic = topic

        self.redis = redis_con

        if not producer:
            self.redis.sadd(KeyPattern.consumers(topic), consumer_id)

    def request(self, data):
        request_id = str(uuid.uuid4())

        # Get consumers
        consumers = self.redis.smembers(KeyPattern.consumers(self.topic))

        # Set request data
        self.redis.hmset(KeyPattern.request(self.topic, request_id), data)

        # Notify each consumer
        for consumer in consumers:
            self.redis.rpush(KeyPattern.consumer(self.topic, consumer), request_id)

        # Poll for responses
        def has_responses():
            for consumer in consumers:
                if not self.redis.exists(KeyPattern.response(self.topic, consumer, request_id)):
                    return False

            return True

        polling.poll(
            has_responses,
            step=0.5,
            timeout=3
        )

        # Get all responses
        resps = []
        for consumer in consumers:
            ret = self.redis.hgetall(KeyPattern.response(self.topic, consumer, request_id))
            resps.append(ret)

        return resps

    def process(self, handler):
        _, request_id = self.redis.blpop(KeyPattern.consumer(self.topic, self.consumer_id))

        request_data = self.redis.hgetall(KeyPattern.request(self.topic, request_id))

        ret = handler(request_data)

        self.redis.hmset(KeyPattern.response(self.topic, self.consumer_id, request_id), ret)
