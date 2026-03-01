from bs4 import BeautifulSoup
from Utils.utils import open_file, save_file, get_user_agent
import requests 
url = 'https://www.skiddle.com/inspire-me/festivals-2026'
main_url_link = 'https://www.skiddle.com'
headers_ = {'User-Agent': get_user_agent()}
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

for festival_link in festivals_links:
    print(festival_link)
    print('-----------------------------')
    response = requests.get(festival_link, headers=get_user_agent())
    save_file('Fest/festival.html', response.text) 
    soup = BeautifulSoup(response.text, 'lxml')
    festival_info = soup.find_all('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 css-2re0kq')

    for info in festival_info:
        try:
            rem = info.span.text.strip()
            if rem:
                print(rem)
        except AttributeError:
            continue
        age = info.find(class_='MuiBox-root css-42igfv')
        if age:
            print(age)

