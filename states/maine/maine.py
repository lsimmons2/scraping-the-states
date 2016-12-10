from pymongo import MongoClient
import requests
import bs4
import lxml
import re


mongo_client = MongoClient()

db = mongo_client.econ

#TOWNS

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
    town_to_add['state'] = unicode('Maine')
    town_to_add['type'] = unicode('town')
    match = re.compile(r'(.+)( \()([^)]+)').search(town.text)
    town_to_add['county'] = match.group(3)
    town_to_add['name'] = match.group(1)
    db.munis.insert_one(town_to_add)



#CITIES
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Maine')
#
# with open('./List_of_cities_in_Maine.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_cities_in_Maine.html'), 'r') as f:
    page = f.read()
soup = bs4.BeautifulSoup(page, 'lxml')


cities = soup.find('table', class_='wikitable sortable').find_all('tr')[1:]

for city in cities:
    city_to_add = {}
    cells = city.find_all('td')
    city_to_add['name'] = cells[1].text
    city_to_add['county'] = cells[5].text
    city_to_add['type'] = unicode('city')
    city_to_add['population'] = {}
    city_to_add['population']['2013'] = int(cells[3].text.replace(',',''))
    db.munis.insert_one(city_to_add)
