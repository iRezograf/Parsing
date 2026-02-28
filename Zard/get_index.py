import requests
from Utils.utils import save_file

url = 'https://zard-company.ru'
header = {'Accept': '*/*',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}

response = requests.get(url, headers = header)
print(response.text)
save_file('index.html', response.text)