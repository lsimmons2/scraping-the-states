from pymongo import MongoClient
import requests
import bs4
import lxml

mongo_client = MongoClient()

db = mongo_client.econ


# ======== TOWNS ========
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_towns_in_Connecticut')
#
# with open('./List_of_towns_in_Vermont.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_towns_in_Connecticut.html'), 'r') as f:
    page = f.read()
soup = bs4.BeautifulSoup(page, 'lxml')


towns = soup.find('table', class_='sortable wikitable').find_all('tr')[1:]


for town in towns:
    town_to_add = {}
    cells = town.find_all('td')
    town_to_add['state'] = unicode('Connecticut')
    town_to_add['name'] = cells[0].text
    town_to_add['population'] = {}
    town_to_add['population']['2010'] = int(cells[3].text.replace(',',''))
    town_to_add['county'] = cells[6].text
    town_to_add['type'] = unicode('town')
    db.munis.insert_one(town_to_add)





# ======== CITIES ========
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Connecticut')
#
# with open('./List_of_cities_in_Connecticut.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_cities_in_Connecticut.html'), 'r') as f:
    page = f.read()
soup = bs4.BeautifulSoup(page, 'lxml')


cities = soup.find('table', class_='wikitable sortable').find_all('tr')[1:]

for city in cities:
    city_to_add = {}
    cells = city.find_all('td')
    city_to_add['name'] = cells[0].text
    city_to_add['state'] = unicode('Connecticut')
    city_to_add['county'] = cells[1].text
    city_to_add['population'] = {}
    city_to_add['population'] = int(cells[2].text.replace(',',''))
    city_to_add['type'] = unicode('city')
    db.munis.insert_one(city_to_add)
