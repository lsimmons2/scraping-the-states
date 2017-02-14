import requests
import time
import os
import re



with open('./states.txt', 'r') as f:
    states = f.read().split('\n')[0:-1]

with open('./new_england.txt', 'r') as f:
    new_england = f.read().split('\n')[0:-1]


# print poss_urls
def get_urls(state):
    base = 'https://wikipedia.org/wiki/List_of_'
    return [
    '%stowns_in_%s' % (base, state),
    '%scities_in_%s' % (base, state),
    '%scities_and_towns_in_%s' % (base, state),
    '%smunicipalities_in_%s' % (base, state)
    ]

for url in get_urls('Vermont'):

re.compile()

# for state in states:
#     if state in new_england:
#         continue
#     # state_dir = './states/%s' % state.lower()
#     # os.makedirs(state_dir)
#     urls = get_urls(state)
#     for url in urls:
#         resp = requests.get(url)
#         if resp.status_code == 200:
#             with open('%s/' % state_dir)
#
