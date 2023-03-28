import mysql.connector
import json

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="entry_task"
)

# Get the cursor
mycursor = mydb.cursor()

data = []
with open('categories.json') as f:
    data = json.load(f)

# Insert the data into the database
for category in data:
    sql = "INSERT INTO categories (id, name, parent_category_id, level) VALUES (%s, %s, %s, %s)"
    val = (category['catid'], category['name'], category['parent_catid'], category['level'])
    mycursor.execute(sql, val)
    mydb.commit()

# Close the connection
mydb.close()
mycursor.close()