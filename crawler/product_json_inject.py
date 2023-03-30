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
with open('data.json') as f:
    data = json.load(f)

# Insert the data into the database
for item in tqdm(data["products"]):
    # Insert the product
    insert_product_query = """
        INSERT INTO products (id, title, description)
        VALUES (%s, %s, %s)
    """
    product_values = (item["id"], item["title"], item["description"])
    cursor.execute(insert_product_query, product_values)
    cnx.commit()

    # Insert the product images
    for image_url in item["image_urls"]:
        insert_image_query = """
            INSERT INTO product_images (product_id, image_url)
            VALUES (%s, %s)
        """
        image_values = (item["id"], image_url)
        cursor.execute(insert_image_query, image_values)
        cnx.commit()

    # Insert the product categories
    for category_id in item["category_ids"]:
        insert_category_query = """
            INSERT INTO product_categories (category_id, product_id)
            VALUES (%s, %s)
        """
        category_values = (category_id, item["id"])
        cursor.execute(insert_category_query, category_values)
        cnx.commit()

# Close the database connection
cursor.close()
cnx.close()
print("Done!")