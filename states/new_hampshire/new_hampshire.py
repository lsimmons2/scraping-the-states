from pymongo import MongoClient
import requests
import bs4
import lxml
import sys
import psycopg2
import getpass



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

if sys.argv[1] == 'mongo':
    mongo_client = MongoClient()
    db = mongo_client.econ


    for muni in munis:
        muni_to_add = {}
        cells = muni.find_all('td')
        muni_to_add['name'] = cells[0].text
        muni_to_add['county'] = cells[1].text
        muni_to_add['state'] = unicode('New Hampshire')
        muni_to_add['population'] = {}
        muni_to_add['population']['2010'] = int(cells[3].text.replace(',',''))
        db.munis.insert_one(muni_to_add)

if sys.argv[1] == 'postgres':

    try:
        conn = psycopg2.connect("dbname='states' user='%s' host='localhost'" % getpass.getuser())
        print 'connected to db!'
    except:
        print 'can\'t connect to db!'
        sys.exit()

    cur = conn.cursor()

    for muni in munis:
        muni_to_add = {}
        cells = muni.find_all('td')
        muni_to_add['name'] = cells[0].text
        muni_to_add['county'] = cells[1].text
        muni_to_add['type'] = unicode('unknown')
        muni_to_add['state'] = unicode('New Hampshire')
        muni_to_add['population'] = int(cells[3].text.replace(',',''))
        try:
            cur.execute(
            '''INSERT INTO munis (name, state, county, type, population)
            VALUES (%(name)s, %(state)s, %(county)s, %(type)s, %(population)s);''',
            muni_to_add)
            print 'muni %s inserted' % muni_to_add['name']
        except Exception as e:
            print 'can\'t insert muni into db: ', str(e)
            sys.exit()

    conn.commit()
