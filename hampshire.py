import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

organisation = "Hampshire County Council"
telegram_config = "conf/hcc-byways-channel.conf"

class fetcher:

    url = 'https://www.hants.gov.uk/community/publicnotices?keywords=BOAT'

    # common method for all similar classes
    def getByways(self):
        return self.getBywayPage(self.url)

    # class specific method that takes URL as a parameter
    def getBywayPage(self,url):

        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        byways = {}

        for li in soup.find_all('li', class_="add-bottom isotope-item thumbnail"):

            h2 = li.find("h2", class_="remove-bottom")
            textDiv = li.find("div", class_="seven columns offset-by-point-five")

            info = {}
            info["url"] = urljoin(url, h2.a['href'])
            info["title"] = h2.a.string
            info["text"] = h2.a.string.next_element.strip()

            noticeId = info["url"].split("=")[1]

            byways[noticeId] = info


        # look to see if there are more pages of data
        nextPage = soup.find("a", class_="paginate_button", title="Next")

        if nextPage:
            moreByways = self.getBywayPage(nextPage['href'])
            byways = {**byways, **moreByways}

        return byways














