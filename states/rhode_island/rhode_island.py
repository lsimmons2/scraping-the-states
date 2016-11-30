from pymongo import MongoClient
import requests
import bs4
import lxml

mongo_client = MongoClient()

db = mongo_client.econ


# ======== TOWNS ========
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_municipalities_in_Rhode_Island')
#
# with open('./List_of_municipalities_in_Rhode_Island.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_municipalities_in_Rhode_Island.html'), 'r') as f:
    page = f.read()
soup = bs4.BeautifulSoup(page, 'lxml')


towns = []

towns = soup.find('table', class_='wikitable sortable').find_all('tr')[2:-1]

for town in towns:
    town_to_add = {}
    cells = town.find_all('td')
    town_to_add['state'] = 'Rhode Island'
    town_to_add['name'] = cells[0].text
    town_to_add['type'] = cells[1].text.lower()
    town_to_add['county'] = cells[2].text
    town_to_add['incorporated'] = cells[3].text
    town_to_add['population'] = cells[5].text
    db.munis.insert_one(town_to_add)
