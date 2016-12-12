from pymongo import MongoClient
import requests
import bs4
import lxml
import sys
import psycopg2
import getpass


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


if sys.argv[1] == 'mongo':

    print 'mongo brah!'

    mongo_client = MongoClient()
    db = mongo_client.econ

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

if sys.argv[1] == 'postgres':

    print 'postgres brah!'

    try:
        conn = psycopg2.connect("dbname='states' user='%s' host='localhost'" % getpass.getuser())
        print 'connected to db!'
    except:
        print 'can\'t connect to db!'
        sys.exit()

    cur = conn.cursor()

    count = 0
    for muni in munis:
        cells = muni.find_all('td')
        municipality = {}
        municipality['state'] = unicode('Massachusetts')
        municipality['name'] = cells[0].text
        municipality['type'] = cells[1].text
        municipality['county'] = cells[2].text
        municipality['population'] = int(cells[4].text.replace(',', ''))
        try:
            cur.execute(
            '''INSERT INTO munis (name, state, county, type, population)
            VALUES (%(name)s, %(state)s, %(county)s, %(type)s, %(population)s);''',
            municipality)
            print 'muni #%s inserted' % count
            count += 1
        except Exception as e:
            print 'can\'t insert muni into db: ', str(e)
            sys.exit()

    conn.commit()
