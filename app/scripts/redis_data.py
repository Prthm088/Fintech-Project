import json
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

for key in r.keys("*"):
    key_type = r.type(key)
    
    print(f"\n Key: {key}")
    print(f" Type: {key_type}")

    if key_type == "string":
        print(r.get(key))

    elif key_type == "hash":
        data = r.hgetall(key)
        try:
            print({k: json.loads(v) for k, v in data.items()})
        except:
            print(data)

    elif key_type == "list":
        print(r.lrange(key, 0, -1))

    elif key_type == "set":
        print(r.smembers(key))

    elif key_type == "zset":
        print(r.zrange(key, 0, -1, withscores=True))

    print("-" * 40)