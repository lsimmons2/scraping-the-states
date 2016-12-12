from pymongo import MongoClient
import requests
import bs4
import lxml
import sys
import psycopg2
import getpass



# ======== TOWNS ========
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_towns_in_Connecticut')
#
# with open('./List_of_towns_in_Vermont.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_towns_in_Connecticut.html'), 'r') as f:
    page = f.read()
soup = bs4.BeautifulSoup(page, 'lxml')


towns = soup.find('table', class_='sortable wikitable').find_all('tr')[1:]

if sys.argv[1] == 'mongo':

    mongo_client = MongoClient()
    db = mongo_client.econ

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

if sys.argv[1] == 'postgres':

    try:
        conn = psycopg2.connect("dbname='states' user='%s' host='localhost'" % getpass.getuser())
        print 'connected to db!'
    except:
        print 'can\'t connect to db!'
        sys.exit()

    cur = conn.cursor()

    count = 0
    for town in towns:
        town_to_add = {}
        cells = town.find_all('td')
        town_to_add['state'] = unicode('Connecticut')
        town_to_add['name'] = cells[0].text
        town_to_add['population'] = int(cells[3].text.replace(',',''))
        town_to_add['county'] = cells[6].text
        town_to_add['type'] = unicode('town')
        try:
            cur.execute(
            '''INSERT INTO munis (name, state, county, type, population)
            VALUES (%(name)s, %(state)s, %(county)s, %(type)s, %(population)s);''',
            town_to_add)
            print 'muni #%s inserted' % count
            count += 1
        except Exception as e:
            print 'can\'t insert muni into db: ', str(e)
            sys.exit()

    conn.commit()



# ======== CITIES ========
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Connecticut')
#
# with open('./List_of_cities_in_Connecticut.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_cities_in_Connecticut.html'), 'r') as f:
    page = f.read()
soup = bs4.BeautifulSoup(page, 'lxml')


cities = soup.find('table', class_='wikitable sortable').find_all('tr')[1:]

if sys.argv[1] == 'mongo':

    mongo_client = MongoClient()
    db = mongo_client.econ

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

if sys.argv[1] == 'postgres':

    try:
        conn = psycopg2.connect("dbname='states' user='%s' host='localhost'" % getpass.getuser())
        print 'connected to db!'
    except:
        print 'can\'t connect to db!'
        sys.exit()

    cur = conn.cursor()

    count = 0
    for town in towns:
        city_to_add = {}
        cells = city.find_all('td')
        city_to_add['name'] = cells[0].text
        city_to_add['state'] = unicode('Connecticut')
        city_to_add['county'] = cells[1].text
        city_to_add['population'] = int(cells[2].text.replace(',',''))
        try:
            cur.execute(
            '''INSERT INTO munis (name, state, county, type, population)
            VALUES (%(name)s, %(state)s, %(county)s, %(type)s, %(population)s);''',
            city_to_add)
            print 'muni #%s inserted' % count
            count += 1
        except Exception as e:
            print 'can\'t insert muni into db: ', str(e)
            sys.exit()

    conn.commit()
