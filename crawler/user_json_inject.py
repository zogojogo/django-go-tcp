import mysql.connector
import json
from tqdm import tqdm

# Connect to MySQL
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="entry_task"
)

# Get the cursor
cursor = cnx.cursor()

data = []
with open('users_5.json') as f:
    data = json.load(f)

for user in tqdm(data):
    sql = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
    val = (user['email'], user['username'], user['password'])
    cursor.execute(sql, val)
    cnx.commit()

cursor.close()
cnx.close()
print("Done!")