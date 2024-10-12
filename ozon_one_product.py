from selenium import webdriver
# класс для указания типа селектора
from selenium.webdriver.common.by import By
# класс для ожидания наступления события
from selenium.webdriver.support.ui import WebDriverWait
# включает проверки, такие как видимость элемента на странице, доступность элемента для отклика и т.п.
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from urllib.parse import unquote_plus

user_agent = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
)

chrome_option = Options()
chrome_option.add_argument(f'user-agent={user_agent}')
chrome_option.add_argument('start-maximized')  # хром на весь экран

driver = webdriver.Chrome(options=chrome_option)
url = 'https://www.ozon.ru/product/timio-f152g-new-noutbuk-15-6-intel-celeron-n5095-ram-8-gb-ssd-256-gb-intel-uhd-graphics-750-1660340013/?advert=LSsFWRANeI4H_gc_v7otEehFXXjQIz5ymD3JhBIc5ppBO3yUDPZnz3MilkPykyx4Q7bOLPcytuzie17BDAF83gPILmngZztLVKTCkpPRokYFU4H7ondpKIR_r86MZ09CtqeGLhrDvcKpo2c927dDVyT6sn0NuIin-lC9yvcva6DdTM6Xw5OSREUMaFWvhYMeaPXorMCSLuNkOGrAYryi32CayhDKt4R4PZwS8VxTli4UKetfsb3_gxk0XKfTcHQTn2apuzEUsz9UW46_A7BmpmjsCeflCGWi3-K38NAFHCGGTfsQkgcH7IG7vj9bVX8v-dWVX1JiJbZrQUHztquAU8MG9Rw9VGVZ6xxXs5AXReiVsEq4IVOHY1qD1N96mZArUnl1mgzh_t7YBWNZPTJmsYPaAx-D_kTUoWSYrg&avtc=1&avte=4&avts=1725809076&keywords=ноутбук'

driver.get(url)
time.sleep(2)

# Находим поле для обновить
reload_button = driver.find_element(By.ID, "reload-button")
reload_button.click()
#
# # Находим поле для поиска
# search_box = driver.find_element(By.XPATH, "//input[@placeholder='Искать на Ozon']")
# # # вставляем в это поле слово которое хотим найти
# search_box.send_keys(search_category)
# # нажатие кнопки поиска
# search_box.submit()
# # ожидаем загрузки страницы
time.sleep(5)

# # Находим поле для поиска
# search_box = driver.find_element(By.XPATH, "//button[contains(@data-link,'Все характеристики и описание')]")
# search_box.click()
# # ожидаем загрузки страницы
# time.sleep(5)

product_data = {}
try:
    product_price = driver.find_element(By.XPATH, "//div[contains(@data-widget,'webPrice')]")
    price = product_price.text
except:
    price = 'не найдено'
try:
    product_name = driver.find_element(By.XPATH, "//h1[contains(@class,'pm9_27')]")
    name = product_name.text.strip().replace(' ', '').replace('₽', '')
except:
    name = 'не найдено'

product_data[name] = {'price': price}
print(product_data)
# with open('wb_product.json', 'w', encoding='UTF-8', newline='') as f:
#     json.dump(books_data, f, ensure_ascii=False, indent=4)
print('Данные сохранены в фай ozon_one_page.json')

driver.close()
