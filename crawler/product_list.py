from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
import json
from faker import Faker

count = 17250 + 1

def get_product_per_category(driver, category_url):
    global count
    driver.get(category_url)
    products = []
    total_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.shopee-mini-page-controller__total'))).text
    for i in range (0, int(total_page)):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.col-xs-2-4.shopee-search-item-result__item')))

        total_page_height = driver.execute_script("return document.body.scrollHeight")
        browser_window_height = driver.get_window_size(windowHandle='current')['height']
        current_position = driver.execute_script('return window.pageYOffset')
        while total_page_height - current_position > browser_window_height:
            time.sleep(0.5)
            driver.execute_script(f"window.scrollTo({current_position}, {browser_window_height + current_position});")
            current_position = driver.execute_script('return window.pageYOffset')

        product_elements = driver.find_elements(by=By.CSS_SELECTOR, value='.col-xs-2-4.shopee-search-item-result__item')

        for product in product_elements:
            name = WebDriverWait(product, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._1yN94N.WoKSjC._2KkMCe')))
            name_text = name.text
            image = WebDriverWait(product, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.B0Ze3i.wAkToc')))
            image_url = image.get_attribute('src')
            category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.shopee-category-list__sub-category.shopee-category-list__sub-category--active'))).get_attribute('href')
            category_id = category.split('.')[-1]
            description = fake.text(
                max_nb_chars=200,
                ext_word_list=None
            )

            product_data = {'id': count, 'title': name_text, 'image_urls': [image_url], 'category_ids' : [category_id], 'description': description}
            products.append(product_data)
            count += 1
        if i < int(total_page) - 1:
            driver.get(f'{category_url}?page={i+1}')
    return products

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    fake = Faker('id_ID')

    base_url = 'https://shopee.co.id'

    links = []
    with open('category_links copy.json') as f:
        links = json.load(f)

    for link in links:
        category_url = f'{base_url}/{link}'
        prods = get_product_per_category(driver, category_url)
        with open(f'products/{link}.json', "w") as outfile:
            json.dump(prods, outfile, indent=4)

    driver.quit()
