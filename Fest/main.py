import random
import time

from bs4 import BeautifulSoup
from Utils.utils import open_file, save_file, get_user_agent
import requests 
url = 'https://www.skiddle.com/inspire-me/festivals-2026'
main_url_link = 'https://www.skiddle.com'
headers = {'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}

# response = requests.get(url, headers=headers)
# save_file('Fest/festivals.html', response.text) 
# print(open_file('Fest/festivals.html'))
soup = BeautifulSoup(open_file('Fest/festivals.html'), 'lxml')
card_details_links = soup.find_all('a', class_='card-details-link')

festivals_links = []
for link in card_details_links:
    festivals_links.append(main_url_link + link['href'].strip())
# print(festivals_links[:1])

save_file('Fest/festivals_links.txt', '\n'.join(festivals_links))
time.sleep(random.uniform(4, 6))

for festival_link in festivals_links[17:19]:
    print(festival_link)
    print('-----------------------------')
    response = requests.get(festival_link, headers = headers)
    time.sleep(random.uniform(4, 6))
    print(response.status_code)
    save_file('Fest/festival.html', response.text) 
    soup = BeautifulSoup(response.text, 'lxml')
    festival_info = soup.find_all('div', class_='css-twt0ol')
    # Использую только первых 4 элемента, 
    # так как там есть вся основная информация о фестивале.

    if not festival_info:
        print("No festival info found for this link.")
        continue
    try:
        data_start = festival_info[0].find('span')
        if data_start:
                print(data_start.text.strip())
    except AttributeError:
        continue

    try:    
        data_start = festival_info[1].find('span')
        if data_start:
                print(data_start.text.strip())
    except AttributeError:
        continue

    try:
        t = festival_info[2]
        if t:
            print(t.text.strip())
    except AttributeError:
            continue
    
    try:
        age = festival_info[3]
        if age:
            print(age.text.strip())
    except AttributeError:
            continue
    print('-----------------------------')
    