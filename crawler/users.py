from faker import Faker
import json
from tqdm import tqdm

fake = Faker('id_ID')

users = []
password_hashed = "$2a$04$qFl2KcE0cqVkalGigFkf2OPrRSD.EtwQqxvRb/2Gfvze4dV8/nQLq"
for i in tqdm(range(6000000, 8000000)):
    username = fake.user_name()
    unique_uname = f'{username}.{i}'
    user = {
        'id': i,
        'username': unique_uname,
        'email': f'{unique_uname}@blanche.life',
        'password': password_hashed,
    }
    users.append(user)

with open('users_5.json', 'w') as f:
    json.dump(users, f, indent=4)