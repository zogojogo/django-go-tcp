from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import json

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

base_url = 'https://shopee.co.id/all_categories'
driver.get(base_url)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'alphabetical-list-of-categories')))

category_elements = driver.find_elements(by=By.CLASS_NAME, value='a-sub-category--display-name')
category_urls = []
for category in category_elements:
    url = category.get_attribute('href')
    trimmed_url = url.split('https://shopee.co.id/')[-1]
    category_urls.append(trimmed_url)

driver.quit()

print(category_urls)
with open('category_links.json', 'w') as f:
    json.dump(category_urls, f, indent=4)