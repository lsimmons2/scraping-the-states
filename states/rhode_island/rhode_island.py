from pymongo import MongoClient
import requests
import bs4
import lxml

mongo_client = MongoClient()

db = mongo_client.econ


# ======== CITIES AND TOWNS ========
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_municipalities_in_Rhode_Island')
#
# with open('./List_of_municipalities_in_Rhode_Island.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_municipalities_in_Rhode_Island.html'), 'r') as f:
    page = f.read()
soup = bs4.BeautifulSoup(page, 'lxml')


munis = soup.find('table', class_='wikitable sortable').find_all('tr')[2:-1]

for muni in munis:
    muni_to_add = {}
    cells = muni.find_all('td')
    muni_to_add['state'] = unicode('Rhode Island')
    muni_to_add['name'] = cells[0].text
    muni_to_add['type'] = cells[1].text
    muni_to_add['county'] = cells[2].text
    muni_to_add['population'] = {}
    muni_to_add['population']['2010'] = int(cells[5].text.replace(',', ''))
    muni_to_add['population']['2000'] = int(cells[6].text.replace(',', ''))
    db.munis.insert_one(muni_to_add)
