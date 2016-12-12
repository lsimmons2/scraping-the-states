from pymongo import MongoClient
import requests
import bs4
import lxml
import re
import sys
import psycopg2
import getpass




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

if sys.argv[1] == 'mongo':

    mongo_client = MongoClient()
    db = mongo_client.econ

    for town in towns:
        town_to_add = {}
        town_to_add['state'] = unicode('Maine')
        town_to_add['type'] = unicode('town')
        match = re.compile(r'(.+)( \()([^)]+)').search(town.text)
        town_to_add['county'] = match.group(3)
        town_to_add['name'] = match.group(1)
        db.munis.insert_one(town_to_add)

if sys.argv[1] == 'postgres':

    try:
        conn = psycopg2.connect("dbname='states' user='%s' host='localhost'" % getpass.getuser())
        print 'connected to db!'
    except:
        print 'can\'t connect to db!'
        sys.exit()

    cur = conn.cursor()

    for town in towns:
        town_to_add = {}
        town_to_add['state'] = unicode('Maine')
        town_to_add['type'] = unicode('town')
        match = re.compile(r'(.+)( \()([^)]+)').search(town.text)
        town_to_add['county'] = match.group(3)
        town_to_add['name'] = match.group(1)
        town_to_add['population'] = 0
        try:
            cur.execute(
            '''INSERT INTO munis (name, state, county, type, population)
            VALUES (%(name)s, %(state)s, %(county)s, %(type)s, %(population)s);''',
            town_to_add)
            print 'muni %s inserted' % town_to_add['name']
        except Exception as e:
            print 'can\'t insert muni into db: ', str(e)
            sys.exit()

    conn.commit()

#CITIES
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Maine')
#
# with open('./List_of_cities_in_Maine.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_cities_in_Maine.html'), 'r') as f:
    page = f.read()
soup = bs4.BeautifulSoup(page, 'lxml')


cities = soup.find('table', class_='wikitable sortable').find_all('tr')[1:]

if sys.argv[1] == 'mongo':

    mongo_client = MongoClient()
    db = mongo_client.econ

    for city in cities:
        city_to_add = {}
        cells = city.find_all('td')
        city_to_add['name'] = cells[1].text
        city_to_add['county'] = cells[5].text
        city_to_add['type'] = unicode('city')
        city_to_add['population'] = {}
        city_to_add['population']['2013'] = int(cells[3].text.replace(',',''))
        db.munis.insert_one(city_to_add)


if sys.argv[1] == 'postgres':

    try:
        conn = psycopg2.connect("dbname='states' user='%s' host='localhost'" % getpass.getuser())
        print 'connected to db!'
    except:
        print 'can\'t connect to db!'
        sys.exit()

    cur = conn.cursor()

    for city in cities:
        city_to_add = {}
        cells = city.find_all('td')
        city_to_add['name'] = cells[1].text
        city_to_add['county'] = cells[5].text
        city_to_add['type'] = unicode('city')
        city_to_add['population'] = int(cells[3].text.replace(',',''))
        try:
            cur.execute(
            '''INSERT INTO munis (name, state, county, type, population)
            VALUES (%(name)s, %(state)s, %(county)s, %(type)s, %(population)s);''',
            city_to_add)
            print 'muni %s inserted' % city_to_add['name']
        except Exception as e:
            print 'can\'t insert muni into db: ', str(e)
            sys.exit()

    conn.commit()
