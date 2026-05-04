import redis
import hashlib
import json

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

        self.ttl = 900  

        self.hits = 0
        self.misses = 0

    def make_key(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def get(self, text):
        key = self.make_key(text)
        data = self.client.get(key)

        if data:
            self.hits += 1
            return json.loads(data)
        else:
            self.misses += 1
            return None

    def set(self, text, value):
        key = self.make_key(text)
        self.client.setex(key, self.ttl, json.dumps(value))

    def stats(self):
        return {
            "hits": self.hits,
            "misses": self.misses
        }