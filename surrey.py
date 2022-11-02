from bs4 import BeautifulSoup
import json
import requests
import hashlib

organisation = "Surrey County Council"
telegram_config = "missing"

class fetcher:

    url = "https://www.surreycc.gov.uk/culture-and-leisure/countryside/management/footpaths-byways-and-bridleways/rights-of-way-public-notices"

    def getByways(self):

        html_text = requests.get(self.url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        byways = {}

        for h2 in soup.find_all('h2'):
            ul = h2.next_sibling
            if ul.name != "ul":
                continue
     
            for li in ul.children:
                if "yway" in li.a.string:
                    is_byway = True
                elif "BOAT" in li.a.string:
                    is_byway = True
                else:
                    is_byway = False

                if is_byway:

                    info = {}
                    info['url'] = li.a['href']
                    info['title'] = li.a.string
                    info['text'] = self.getBywayText(li.a['href'])

                    id = hashlib.md5(info['url'].encode('utf-8')).hexdigest()

                    byways[id] = info

        return byways


    def getBywayText(self, url):

        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        text_fields = []

        for element in soup.article.contents:

            if element.name in ["h2", "h3", "p"]:
                if element.string:
                    text_fields.append(element.string)

            if element.name == "hr":
                break

        return str("\n\n".join(text_fields).encode('utf-8'))
