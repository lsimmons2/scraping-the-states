from pymongo import MongoClient
import requests
import bs4
import lxml
import re
import sys
import psycopg2
import getpass



#
# #TOWNS
# # resp = requests.get('https://en.wikipedia.org/wiki/List_of_towns_in_Vermont')
# #
# # with open('./List_of_towns_in_Vermont.html', 'w') as f:
# #     f.write(resp.text.encode('utf8'))
#
with open(('./List_of_towns_in_Vermont.html'), 'r') as f:
    page = f.read()
soup = bs4.BeautifulSoup(page, 'lxml')


towns = []

towns = soup.find('table', class_='sortable wikitable').find_all('tr')[1:]


if sys.argv[1] == 'mongo':
    mongo_client = MongoClient()
    db = mongo_client.econ

    for town in towns:
        town_to_add = {}
        cells = town.find_all('td')
        town_to_add['state'] = unicode('Vermont')
        town_to_add['name'] = cells[1].text
        town_to_add['county'] = cells[2].text
        town_to_add['population'] = {}
        town_to_add['population']['2000'] = int(cells[3].text)
        if cells[1].text in ['Averill', 'Ferdinand', 'Glastenbury', 'Lewis', 'Somerset']:
            town_to_add['type'] = unicode('unincorporated town')
        else:
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

    for town in towns:
        town_to_add = {}
        cells = town.find_all('td')
        town_to_add['state'] = unicode('Vermont')
        town_to_add['name'] = cells[1].text
        town_to_add['county'] = cells[2].text
        town_to_add['population'] = int(cells[3].text)
        if cells[1].text in ['Averill', 'Ferdinand', 'Glastenbury', 'Lewis', 'Somerset']:
            town_to_add['type'] = unicode('unincorporated town')
        else:
            town_to_add['type'] = unicode('town')
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
# resp = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Vermont')
#
# with open('./List_of_cities_in_Vermont.html', 'w') as f:
#     f.write(resp.text.encode('utf8'))

with open(('./List_of_cities_in_Vermont.html'), 'r') as f:
    page = f.read()

soup = bs4.BeautifulSoup(page, 'lxml')

cities = soup.find('table', class_='sortable wikitable').find_all('tr')[1:]

if sys.argv[1] == 'mongo':

    mongo_client = MongoClient()
    db = mongo_client.econ

    for city in cities:
        city_to_add = {}
        cells = city.find_all('td')
        regex = re.compile(r'(.+)(\[.+])')
        city_to_add['name'] = regex.search(cells[0].text).group(1)
        city_to_add['county'] = cells[2].text
        city_to_add['state'] = unicode('Vermont')
        city_to_add['population'] = {}
        city_to_add['population']['2010'] = int(cells[3].text.replace(',',''))
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

    for city in cities:
        city_to_add = {}
        cells = city.find_all('td')
        regex = re.compile(r'(.+)(\[.+])')
        city_to_add['name'] = regex.search(cells[0].text).group(1)
        city_to_add['county'] = cells[2].text
        city_to_add['state'] = unicode('Vermont')
        city_to_add['population'] = {}
        city_to_add['population']['2010'] = int(cells[3].text.replace(',',''))
        city_to_add['type'] = unicode('city')
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
