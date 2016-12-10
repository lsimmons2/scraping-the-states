from pymongo import MongoClient
import requests
import bs4
import lxml


mongo_client = MongoClient()

db = mongo_client.econ

#CITIES AND TOWNS
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_New_Hampshire')
#
# with open('./List_of_towns_in_New_Hampshire.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))
#

with open(('./List_of_cities_and_towns_in_New_Hampshire.html'), 'r') as f:
    page = f.read()


soup = bs4.BeautifulSoup(page, 'lxml')


munis = soup.find('table', class_='sortable wikitable').find_all('tr')[1:]

for muni in munis:
    muni_to_add = {}
    cells = muni.find_all('td')
    muni_to_add['name'] = cells[0].text
    muni_to_add['county'] = cells[1].text
    muni_to_add['state'] = unicode('New Hampshire')
    muni_to_add['population'] = {}
    muni_to_add['population']['2010'] = int(cells[3].text.replace(',',''))
    db.munis.insert_one(muni_to_add)
