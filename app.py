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

munis = soup.find(id='mw-content-text').find_all('table')[1]

print type(munis)
for muni in munis:
    db.munis.insert_one(muni)
