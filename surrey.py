from bs4 import BeautifulSoup
import hashlib
import json
import os
import requests
import urllib

organisation = "Surrey County Council"
telegramConfig = "conf/surreytrf-group.conf"
#telegramConfig = "conf/telegram/test.conf"

class fetcher:

    url = "https://www.surreycc.gov.uk/culture-and-leisure/countryside/management/footpaths-byways-and-bridleways/rights-of-way-public-notices"

    def getNotices(self):

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

                    article_url = li.a['href']

                    info = {}
                    info['url'] = article_url
                    info['title'] = li.a.string

                    # get extra details from the article page
                    article_html_text = requests.get(article_url).text
                    article_soup = BeautifulSoup(article_html_text, 'html.parser')

                    # build the text blob
                    text_fields = []
                    for element in article_soup.article.contents:

                        if element.name in ["h2", "h3", "p"]:
                            if element.string:
                                text_fields.append(element.string)

                        if element.name == "hr":
                            break

                    info['text'] = str("\n\n".join(text_fields))

                    # any PDF attachments
                    info['attachments'] = {} 
                    for pdf_li in article_soup.find_all("li", class_="resources__item--pdf"):
                        pdf_url = pdf_li.a['href']
                        pdf_file_name = os.path.basename(urllib.parse.urlparse(pdf_url).path)

                        info['attachments'][pdf_file_name] = pdf_url

                    id = hashlib.md5(info['url'].encode('utf-8')).hexdigest()

                    byways[id] = info

        return byways
