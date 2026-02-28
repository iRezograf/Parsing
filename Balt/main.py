import csv
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from Utils.utils import open_file, save_file

main_url_link = 'https://www.baltopttorg.ru'
uagent = UserAgent()
header = {'User-Agent': uagent.chrome}

def get_catalogs(url):
    response = open_file('index.html')
    soup = BeautifulSoup(response,'lxml')
    items = soup.find_all(class_='catalog-nav__element')
    for item in items:
        if item:
            try:
                cat_path = item.find('a').get('href')
                catalog_links.append(url + cat_path)
            except NameError:
                catalog_links.append('')
    return catalog_links

def get_category_links(catalog):
    if catalog_link != 'https://www.baltopttorg.ru/catalogue/178':
        response = requests.get(catalog, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all(class_='category-list__item')
        if items:
            for item in items:
                try:
                    category = item.find('a').get('href')
                    if category:
                        category_links.append(main_url_link + category)
                except NameError:
                    category_links.append('')
    return category_links

def get_card_links(category):
    response = requests.get(category, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all(class_='product-card')
    product_card_links = []
    if items:
        for item in items:
            try:
                card_path = item.find('a', class_='product-card__link').get('href')
                if card_path:
                    product_card_links.append(main_url_link + card_path)
            except NameError:
                product_card_links.append('')

        # print(f'Карточка товара: {card_link}')
    return product_card_links

def get_cards(card):
    response = requests.get(card, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    product_title, product_price, product_amount = '-', '-', '-'
    try:
        product_title = soup.find('h1', class_='product__title').text.strip()
        product_price = soup.find('p', class_='product__price').text.strip().replace("Цена:", "").replace(" ", "")
        product_amount = soup.find('p', class_='product__amount').text.strip().replace("\xa0", " ").replace(
            "В наличии:", "")
        return [product_title, product_price, product_amount]
    except NameError:
        return [product_title, product_price, product_amount]


start_time = time.time()  # Фиксируем время начала
# circle_count = 300

#response = requests.get(url, headers=header)
#save_file('index.html', response.text)


card_info = []
catalog_links = []
limit_cnt_start = 8
limit_cnt_end = 11

if get_catalogs(main_url_link):

    save_file('catalog_links.txt', '\n'.join(catalog_links))
    category_links = []
    for catalog_link in catalog_links[limit_cnt_start:limit_cnt_end]:
        get_category_links(catalog_link)
    save_file('category_links.txt', '\n'.join(category_links))


    card_links = []
    cnt = len(category_links)
    for category_link in category_links:
        print(f'Осталось обработать: {cnt} категорий')
        print(f"Время выполнения: {time.time()-start_time:.2f} секунд")
        card_links = get_card_links(category_link)
        cnt -= 1

        for card_link in card_links:
            try:
                card_information = get_cards(card_link)
                card_info.append(card_information)
                print(card_information)
            except NameError:
                print('Карточка не прочиталась')
            #print(card_info[-1])

with open('products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Наименование', 'Цена', 'Количество'])
    for info in card_info:
        try:
            writer.writerow(info[0:3])  # Записываем первые 3 элемента списка info (название, цена, количество)
        except NameError:
            writer.writerow(['-', '-', '-'])

end_time = time.time()  # Фиксируем время окончания
elapsed_time = end_time - start_time  # Вычисляем затраченное время
print(f"Время выполнения: {elapsed_time:.2f} секунд")