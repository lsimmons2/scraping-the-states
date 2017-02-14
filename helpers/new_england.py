import requests
import time

with open('./new_england.txt', 'r') as f:
    new_england = f.read().split('\n')
    # new_england.pop()
    new_england = new_england[0:-1]


poss_urls = [
'List_of_towns_in_%s' % 'Vermont',
'List_of_cities_in_%s' % 'Vermont',
'List_of_cities_and_towns_in_%s' % 'Vermont',
'List_of_municipalities_in_%s' % 'Vermont'
]

# print poss_urls
def url(endpoint):
    return 'https://wikipedia.org/wiki/%s' % endpoint


count = 0
for i in range(0,4):
    if(i == 0):
        first = requests.get(url(poss_urls[0])).text
        count += 1
    resp = requests.get(url(poss_urls[i])).text
    if(resp == first):
        count += 1
        print 'same'
    time.sleep(1)

print count



# town_resp = requests.get(url(poss_urls[0]))
# muni_resp = requests.get(url(poss_urls[3]))
#
# print len(muni_resp.text)
# print len(town_resp.text)
