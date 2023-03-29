import mysql.connector
import json
from tqdm import tqdm
import os

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="entry_task"
)

cursor = cnx.cursor()
unique_count = 1100000

def insert_product_data(data):
    global unique_count
    for item in tqdm(data, leave=False):
        insert_product_query = """
            INSERT INTO products (id, title, description)
            VALUES (%s, %s, %s)
        """
        product_values = (unique_count, item["title"], item["description"])
        cursor.execute(insert_product_query, product_values)
        cnx.commit()

        for image_url in item["image_urls"]:
            insert_image_query = """
                INSERT INTO product_images (product_id, image_url)
                VALUES (%s, %s)
            """
            image_values = (unique_count, image_url)
            cursor.execute(insert_image_query, image_values)
            cnx.commit()

        for category_id in item["category_ids"]:
            insert_category_query = """
                INSERT INTO product_categories (category_id, product_id)
                VALUES (%s, %s)
            """
            category_values = (category_id, unique_count)
            cursor.execute(insert_category_query, category_values)
            cnx.commit()
        unique_count += 1

if __name__ == "__main__":
    files = os.listdir('products')

    for i in tqdm(range(15)):
        for file in tqdm(files, leave=False):
            file_path = os.path.join('products', file)

            with open(file_path, "r") as f:
                data = json.load(f)
                insert_product_data(data)

    cursor.close()
    cnx.close()
    print("Done!")