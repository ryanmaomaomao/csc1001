import requests
import pandas as pd
from pyquery import PyQuery as pq

# Parent class
class Crawl:
    # constructor with URL
    def __init__(self,url):
        self.url = url        

# Crawling method by one of the member Yinjie
class CrawlByYinjie(Crawl):

    def getURLContent(self):
        # this part is imitate the user-agent and make request
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
        }
        response = requests.post(self.url, headers=headers)
        return response.status_code, response

    def getCountryEpidemiSituationInfo(self):
        # this part is input the URL of json file and get the data
        status_code, data = self.getURLContent()
        data = data.json()
        data = data["data"]
        return data

    def getData(self):
        # organize the data to and convert to pandas dataframe
        # Then modify those wrong negative input to 0
        result = pd.DataFrame(data = self.getCountryEpidemiSituationInfo())
        ind = result[result['confirm_add'] < 0].index
        result.iloc[ind, 1] = 0
        return result


# Crawling method by one of the member Kejin
class CrawlByKejin(Crawl):
    def get_page(self):
        # Get the html source file of that URL
        r = requests.get(self.url)
        r.encoding = 'utf8'
        html = r.text
        return html

    def parse_eco(self):
        text = self.get_page()
        doc = pq(text)  # initialize html source to PyQuery Object

        # Get the 'tr' labels within 'tbody' of the table
        tds = doc('table tbody tr').items()

        # A container for dataframe
        row = []

        for td in tds:

            # Use css path to find the data we need
            rank = td.find('td:first-child').text()  # first td label's text
            country = td.find('td:nth-child(2)').text()  # second td label's text
            continent = td.find('td:nth-child(3)').text()
            population = td.find('td:nth-child(4)').text()
            proportion = td.find('td:nth-child(5)').text()

            # integrate into a list and merge to row container
            col = [rank,country,continent,population,proportion]
            row.append(col)

        # convert to dataframe and set column names
        result = pd.DataFrame(row)
        result.columns = ['rank','country','continent','value','proportion']
        return result

