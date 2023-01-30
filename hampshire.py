from bs4 import BeautifulSoup
import requests
import urllib

organisation = "Hampshire County Council"
telegramConfig = "conf/telegram/hcc-byways-channel.conf"
#telegramConfig = "conf/telegram/test.conf"

class fetcher:

    url = 'https://www.hants.gov.uk/community/publicnotices?keywords=BOAT'

    # common method for all similar classes
    def getNotices(self):
        return self.getNoticePage(self.url)

    # class specific method that takes URL as a parameter
    def getNoticePage(self,url):

        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        byways = {}

        for li in soup.find_all('li', class_="add-bottom isotope-item thumbnail"):

            h2 = li.find("h2", class_="remove-bottom")
            textDiv = li.find("div", class_="seven columns offset-by-point-five")

            info = {}
            info["url"] = urllib.parse.urljoin(url, h2.a['href'])
            info["title"] = h2.a.string
            info["text"] = h2.a.string.next_element.strip()
            info["attachments"] = self.getAttachments(info["url"])

            noticeId = info["url"].split("=")[1]

            byways[noticeId] = info

        # look to see if there are more pages of data
        nextPage = soup.find("a", class_="paginate_button", title="Next")

        if nextPage:
            moreByways = self.getNoticePage(nextPage['href'])
            byways = {**byways, **moreByways}

        return byways

    def getAttachments(self, notice_url):

        attachments = {}

        html_text = requests.get(notice_url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        for row in soup.find_all('div', class_="row"):
            if len(row.contents) == 3 and row.contents[1].name == "a":
                attachment_url = urllib.parse.urljoin(notice_url,row.contents[1]['href'])
                qs = urllib.parse.urlparse(attachment_url).query
                qs_args = urllib.parse.parse_qs(qs)
                file_name = qs_args['attachmentTitle'][0]

                attachments[file_name] = attachment_url

        return attachments
