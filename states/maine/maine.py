from pymongo import MongoClient
import requests
import bs4
import lxml
import re


mongo_client = MongoClient()

db = mongo_client.econ


# resp = requests.get('https://en.wikipedia.org/wiki/List_of_towns_in_Maine')
#
# with open('./List_of_towns_in_Maine.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_towns_in_Maine.html'), 'r') as f:
    page = f.read()


soup = bs4.BeautifulSoup(page, 'lxml')

towns = []

for table in soup.find_all('table', class_='wikitable'):
    towns = towns + table.find_all('tr')[1].find_all('li')

for town in towns:
    town_to_add = {}
    town_to_add['type'] = 'Town'
    town_to_add['state'] = 'Maine'
    town_to_add['county'] = re.search(r'([^\s]+)', town.text).group(1)
    town_to_add['municipality'] = re.search(r'\((.*?)\)', town.text).group(1)
    db.munis.insert_one(town_to_add)
