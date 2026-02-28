import csv

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re

# Beautiful Soup — это библиотека Python для извлечения данных из файлов HTML и XML.
# Она создает дерево парсинга из проанализированного документа,
# которое можно использовать для извлечения данных из HTML,
# что делает ее полезным инструментом для веб-скрапинга.

url = 'https://zard-company.ru'
header = {'Accept': '*/*',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}


# ua = UserAgent()
# print(ua.chrome)  # Выведет случайный UA для Chrome
# print(ua.random)

def open_file(fname):
    with open(fname, 'r') as file:
        src = file.read()
    return src


def save_file(fname, src):
    with open(fname, 'w') as file:
        file.write(src)


def get_catalogs(url):
    # response = requests.get(url, headers = header)
    # save_html('index.html', response.text)
    response = open_file('index.html')

    soup = BeautifulSoup(response,
                         'lxml')  # lxml - это парсер, который использует библиотеку lxml для обработки HTML и XML документов.
    items = soup.find_all(class_='dropdown-submenu')

    catalog_links = []
    for item in items:
        catalog_links.append(url + item.find('a').get('href'))
    save_file('catalog_links.txt', '\n'.join(catalog_links))
    return catalog_links


def get_positions(url):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all(
        class_='col-lg-3 col-md-4 col-sm-6 col-xs-6 col-xxs-12 item item-parent catalog-block-view__item js-notice-block item_block')
    for item in items:
        try:
            title = item.find('a', class_='dark_link js-notice-block__title option-font-bold font_sm').text
            price = item.find('span', class_='price_value').text.replace("\u00A0", "")
            cnt = item.find('span', class_='cnt').text
            print(f'Наименование:  {title} Цена:  {price} за {cnt}')
        except:
            print(f'Наименование:  {title} Без цены')


catalog_links = get_catalogs(url)

# for catalog_link in catalog_links[:3]:
with open('products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Наименование', 'Цена', 'Вес'])
    for catalog_link in catalog_links:
        print(catalog_link)
        response = requests.get(catalog_link, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')

        items = soup.find_all(
            class_='col-lg-3 col-md-4 col-sm-6 col-xs-6 col-xxs-12 item item-parent catalog-block-view__item js-notice-block item_block')
        for item in items:
            try:
                title = item.find('a', class_='dark_link js-notice-block__title option-font-bold font_sm').text
                price = item.find('span', class_='price_value').text.replace("\u00A0", "")
                cnt = item.find('span', class_='cnt').text
                print(f'Наименование:  {title} Цена:  {price} за {cnt}')
                writer.writerow([title, price, cnt])
            except:
                writer.writerow([title, '-', '-'])
                print(f'Наименование:  {title} Без цены')

            # get_catalogs(url)
