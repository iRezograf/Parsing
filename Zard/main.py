import csv
from bs4 import BeautifulSoup
import requests

from Utils.utils import open_file, save_file

url_link = 'https://zard-company.ru'
header_ = {'Accept': '*/*',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}






def get_catalogs(url_link):
    response= open_file('index.html')
    print(response)
    soup = BeautifulSoup(response, 'html.parser')
    items = soup.find_all(class_='dropdown-submenu')
    catalog_links = []
    for item in items:
        catalog_links.append(url_link + item.find('a').get('href'))
    save_file('catalog_links.txt', '\n'.join(catalog_links))
    return catalog_links


def get_positions(url_link):
    response = requests.get(url_link, headers=header_)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all(
        class_='col-lg-3 col-md-4 col-sm-6 col-xs-6 col-xxs-12 item item-parent catalog-block-view__item js-notice-block item_block')
    for item in items:
        title = ''
        try:
            title = item.find('a', class_='dark_link js-notice-block__title option-font-bold font_sm').text
            price = item.find('span', class_='price_value').text.replace("\u00A0", "")
            cnt = item.find('span', class_='cnt').text
            print(f'Наименование:  {title} Цена:  {price} за {cnt}')
        except:
            print(f'Наименование:  {title} Без цены')


catalog_links = get_catalogs(url_link)
# for catalog_link in catalog_links[:3]:
with open('products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Наименование', 'Цена', 'Вес'])
    for catalog_link in catalog_links:
        print(catalog_link)
        response = requests.get(catalog_link, headers=header_)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.find_all(
            class_='col-lg-3 col-md-4 col-sm-6 col-xs-6 col-xxs-12 item item-parent catalog-block-view__item js-notice-block item_block')
        for item in items:
            title = ''
            try:
                title = item.find('a', class_='dark_link js-notice-block__title option-font-bold font_sm').text
                price = item.find('span', class_='price_value').text.replace("\u00A0", "")
                cnt = item.find('span', class_='cnt').text
                print(f'Наименование:  {title} Цена:  {price} за {cnt}')
                writer.writerow([title, price, cnt])
            except:
                writer.writerow([title, '-', '-'])
                print(f'Наименование:  {title} Без цены')

