import mysql.connector
import json
from tqdm import tqdm
import os
from faker import Faker

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="entry_task"
)

cursor = cnx.cursor()
unique_count = 2250000
user_id_mock = 10022382

def insert_product_comments(data, fake):
    global unique_count
    for item in tqdm(data["SELECT p.id from products p "], leave=False):
        for i in range(2):
            insert_product_comment_query = """
            INSERT INTO product_comments (id, product_id, user_id, comment_text)
            VALUES (%s, %s, %s, %s)
            """
            product_comment_values = (unique_count, item["id"], user_id_mock, fake.text(max_nb_chars=50))
            cursor.execute(insert_product_comment_query, product_comment_values)
            cnx.commit()
            unique_count += 1
        insert_child_product_comment_query = """
        INSERT INTO product_comments (id, product_id, user_id, comment_text, parent_comment_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        product_comment_values = (unique_count, item["id"], user_id_mock, fake.text(max_nb_chars=50), unique_count-1)
        cursor.execute(insert_child_product_comment_query, product_comment_values)
        cnx.commit()
        unique_count += 1

if __name__ == "__main__":
    fake = Faker()
    files = os.listdir('product_ids')

    for file in tqdm(files, leave=False):
        file_path = os.path.join('product_ids', file)

        with open(file_path, "r") as f:
            data = json.load(f)
            insert_product_comments(data, fake)

    cursor.close()
    cnx.close()
    print("Done!")

