url = 'https://www.skiddle.com/inspire-me/festivals-2026'
from Utils.utils import open_file, save_file, get_user_agent
import requests 
headers = {'User-Agent': get_user_agent()}
response = requests.get(url, headers=headers)
save_file('Fest/festivals.html', response.text) 
print(open_file('festivals.html'))
