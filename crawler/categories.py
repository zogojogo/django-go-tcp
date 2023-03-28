import requests
import json

url = "https://shopee.co.id/api/v4/pages/get_category_tree"

response = requests.request("GET", url)
data = json.loads(response.text)

def extract_categories(categories, parent_catid=None, level=1):
    result = []
    for category in categories:
        catid = category["catid"]
        name = category["name"]
        result.append({"catid": catid, "name": name, "parent_catid": parent_catid, "level": level})
        if "children" in category and category["children"] is not None:
            result.extend(extract_categories(category["children"], parent_catid=catid, level=level+1))
    return result

categories = data['data']['category_list']
categories = extract_categories(categories)

with open('categories.json', 'w') as f:
    json.dump(categories, f, indent=4)