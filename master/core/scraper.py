from bs4 import BeautifulSoup
import requests
import databaser
from time import sleep
import urllib2
import config

class Extractor:
    def __init__(self):
        self.cf = config.Config

    def getIdsAndTokens(self, html):
        soup = BeautifulSoup(html, "lxml")
        divs = soup.findAll('div', {'class': 'id3'})
        links = []
        for div in divs:
            links.append(div.find('a').get('href'))
        idsAndTokens = {}
        for link in links:
            link_data = link.split("/")
            idsAndTokens.update({link_data[4]: link_data[5]})
            #print link_data
        return zip(idsAndTokens.keys(), idsAndTokens.values())

    def createJsonString(self, gidList):
        jsonPre = '{ "method":"gdata", "namespace":"1", "gidlist":['
        strList = []
        for gid in gidList:
            str = '[' + gid[0] + ',"' + gid[1] + '"],\n'
            strList.append(str)
        jsonPost = ']}'
        return jsonPre + ''.join(strList)[:-2] + jsonPost

    def main(self, html, dbr):
        links = open(html)
        ids = self.getIdsAndTokens(links)
        # Rate limit ids passed in and posted
        chunked_ids = self.chunks(ids, 20)
        for chunk in chunked_ids:
            data = self.createJsonString(chunk)
            dbr.addJsonInput(self.hitApi(data))

    def hitApi(self, data):
        sleep(5)  # Time in seconds
        apiResults = requests.post(cf.url, data=data).content
        return apiResults


    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in xrange(0, len(l), n):
            yield l[i:i + n]

if __name__ == "__main__":
    extractor = Extractor()
    dbr = databaser.Databaser()

    response = urllib2.urlopen('http://www.example.com/')
    html = response.read()
    extractor.main(html, dbr)
    #extractor.main("page.html", dbr)



