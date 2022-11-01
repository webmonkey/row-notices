#!/usr/bin/python3

from bs4 import BeautifulSoup
import json
import requests
import telegram_send
from urllib.parse import urljoin

url = 'https://www.hants.gov.uk/community/publicnotices?keywords=BOAT'

def getByways(url):

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    byways = {}

    for h2 in soup.find_all('h2', class_="remove-bottom"):
        # convert relative URL to absolute
        noticeUrl = urljoin(url, h2.a['href'])

        byways[h2.a.string] = noticeUrl 


    # look to see if there are more pages of data
    nextPage = soup.find("a", class_="paginate_button", title="Next")

    if nextPage:
        moreByways = getByways(nextPage['href'])
        byways = {**byways, **moreByways}

    return byways



print("Starting...")

currentByways = getByways(url)


print(currentByways)

print(str(len(currentByways)) +" current byways")

print("Exiting...")
