from selenium import webdriver
# класс для указания типа селектора
from selenium.webdriver.common.by import By
# класс для ожидания наступления события
from selenium.webdriver.support.ui import WebDriverWait
# включает проверки, такие как видимость элемента на странице, доступность элемента для отклика и т.п.
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
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

url = 'https://www.ozon.ru/'
search_category = 'ноутбук'
driver.get(url)
time.sleep(5)

while True:
    try:
        # Находим поле для поиска
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='Искать на Ozon']")
        # # вставляем в это поле слово которое хотим найти
        search_box.send_keys(search_category)
        # нажатие кнопки поиска
        search_box.submit()
        # ожидаем загрузки страницы
        time.sleep(5)

        # проверка что слово есть в заголовке, значит открылась нужная страница
        search_results = driver.current_url.split('=')[-1]
        res = unquote_plus(search_results, encoding="utf-8")
        assert search_category in res

        # ожидаем подгрузку всех элементов тела
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # прокурчиваем до конца экрана
        scroll_pause = 2
        page_height = driver.execute_script('return document.documentElement.scrollHeight')  # высота экрана
        while True:
            driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
            time.sleep(scroll_pause)
            new_height = driver.execute_script('return document.documentElement.scrollHeight')
            if new_height == page_height:
                break
            page_height = new_height

        # создаем список, куда будем заносить данные по продукции в виде словаря
        products_data_list = []
        time.sleep(5)

        # создаем цикл, для получения не более тысячи позиций продукции
        while len(products_data_list) < 1000:
            # находим все карточки товара на странице (название классов обновляется, поэтому нужно проверять)
            products_list = driver.find_elements(By.XPATH, "//div[@class='jr9_23 j9r_23']")
            for product in products_list:
                product_dict = {}  # создаем словарь для внесения информации по товару
                try:
                    # получаем наименование товара
                    product_name = product.find_element(By.XPATH, ".//span[@class='tsBody500Medium']")
                    name = product_name.text.strip().replace(r"\\", "")
                except:
                    name = 'отсутствуют данные по названию'
                product_dict['Наименование'] = name
                try:
                    # получаем цену товара
                    product_price = product.find_element(By.XPATH, ".//span[@class='c3017-a1 tsHeadline500Medium c3017-c0']")
                    data = product_price.text.replace(' ', '').replace('₽', '').split('\n')
                    price = int(data[0])
                except:
                    price = 'отсутствуют данные по цене'
                product_dict['Цена по карте Озон'] = price
                try:
                    # получаем данные по характеристикам товара
                    product_data = product.find_element(By.XPATH, ".//span[@class='tsBody400Small']")
                    all_info = product_data.text.strip()
                    info_list = all_info.split('\n')
                    for info in info_list:
                        data = info.split(':')
                        product_dict[data[0].strip()] = data[1].strip()
                except:
                    product_dict['Прочая информация'] = 'отсутствуют данные по прочей информации'
                product_dict['Дата'] = datetime.datetime.now().strftime("%d-%m-%Y")
                products_data_list.append(product_dict)
            # ищем кнопку дальше
            try:
                next_button = driver.find_element(By.XPATH, "//a[@class='re8 b2115-a0 b2115-b6 b2115-b1']")

                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(1)  # делаем паузу для исключения перегрузки сервера и отрицательного воздействия на сайт
            except Exception as e:
                print("Больше страниц нет или произошла ошибка:", e)
                break
        break
    except:
        # Нажимаем на кнопку обновить (защита от роботизации поиска)
        reload_button = driver.find_element(By.ID, "reload-button")
        reload_button.click()

# записываем получившиеся данные в файл json
with open(f'ozon_one_page_list_all_page_{datetime.datetime.now().strftime("%d-%m-%Y")}.json', 'w', encoding='UTF-8', newline='') as f:
    json.dump(products_data_list, f, ensure_ascii=False, indent=4)
print(f'Данные сохранены в фай ozon_one_page_list_all_page_{datetime.datetime.now().strftime("%d-%m-%Y")}.json')
driver.close()
