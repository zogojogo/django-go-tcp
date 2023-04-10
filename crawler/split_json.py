import json
import random

with open('users/users_2.json') as f:
    data = json.load(f)

sample = random.sample(data, 200)

with open('users_200.json', 'w') as f:
    json.dump(sample, f)