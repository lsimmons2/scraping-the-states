
import requests
import bs4
import lxml
import re
from time import sleep
import webbrowser

# resp = requests.get('http://state.1keydata.com/')
# soup = bs4.BeautifulSoup(resp.text, 'lxml')


# with open('../states.txt', 'r') as f:
#     states = f.read().split('\n')[0:-1]
#
# for state in states:
#     print state
#     sleep(2)
#
#
# def get_urls(state):
#     base = 'https://en.wikipedia.org/wiki/List_of_'
#     return [
#     '%stowns_in_%s' % (base, state),
#     '%scities_in_%s' % (base, state),
#     '%scities_and_towns_in_%s' % (base, state),
#     '%smunicipalities_in_%s' % (base, state)
#     ]
#
string = 'Massachusetts is a state located in Northeastern United States.'
#
# def try_urls(state):
#     poss_urls = get_urls(state)
#     for url in poss_urls:
#         print url
#         resp = requests.get(url).url
#         soup = bs4.BeautifulSoup(resp.text, 'lxml')
#         if soup.find(string):
#             print 'sah'
#         print '\n'
#         sleep(1)
#
#
# print try_urls('Massachusetts')

resp = requests.get('https://en.wikipedia.org/wiki/List_of_municipalities_in_Massachusetts')

soup = bs4.BeautifulSoup(resp.text, 'lxml')
print soup.find(string)
