import requests
import bs4
import lxml
import re



resp = requests.get('http://state.1keydata.com/')
soup = bs4.BeautifulSoup(resp.text, 'lxml')


with open('./states.txt', 'w') as f:
    for i in range (1,5):
        col = 'col%s' % i
        for state in soup.find(id=col).find_all('a'):
            f.write('%s\n' % state.text)
