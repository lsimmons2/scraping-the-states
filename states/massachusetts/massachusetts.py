from pymongo import MongoClient
import requests
import bs4
import lxml

mongo_client = MongoClient()

db = mongo_client.econ


#CITIES AND TOWNS
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_municipalities_in_Massachusetts')
#
#
# with open('./List_of_municipalities_in_Massachusetts.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_municipalities_in_Massachusetts.html'), 'r') as f:
    page = f.read()


soup = bs4.BeautifulSoup(page, 'lxml')

munis = soup.find(class_="wikitable sortable").find_all('tr')[1:]

for muni in munis:
    cells = muni.find_all('td')
    municipality = {}
    municipality['state'] = unicode('Massachusetts')
    municipality['name'] = cells[0].text
    municipality['type'] = cells[1].text
    municipality['county'] = cells[2].text
    municipality['population'] = {}
    municipality['population']['2010'] = int(cells[4].text.replace(',', ''))
    db.munis.insert_one(municipality)
