import json
import random

def test():
    data = {
        "val": 10
    }

    payload = json.dumps(data).encode("utf-8")

    a = 10

    print(payload)

    print(len(payload))

def get_random():
    return random.randint(1, 3)


print(get_random())
print(get_random())
print(get_random())
print(get_random())