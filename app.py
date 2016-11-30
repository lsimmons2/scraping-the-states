from pymongo import MongoClient
import requests
import bs4
import lxml

mongo_client = MongoClient()

db = mongo_client.econ

#
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_municipalities_in_Massachusetts')
#
#
# with open(('./resp'), 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./resp'), 'r') as f:
    page = f.read()


soup = bs4.BeautifulSoup(page, 'lxml')

munis = soup.find(class_="wikitable sortable").find_all('tr')[1:]

for muni in munis:
    cells = muni.find_all('td')
    municipality = {}
    municipality['state'] = 'Massachusetts'
    municipality['municipality'] = cells[0].text
    municipality['type'] = cells[1].text
    municipality['county'] = cells[2].text
    municipality['population'] = cells[4].text
    municipality['established'] = cells[5].text
    db.munis.insert_one(municipality)
