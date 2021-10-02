import json
from bs4 import BeautifulSoup as BSoup

class Module :
    def __init__(self, title,  baseUrl, parentScrapper):
        self.title = title
        self.codeName = baseUrl.split('/')[4]
        self.baseUrl = baseUrl
        self.scrapper = parentScrapper

    def dump(self):
        output = {
            "title"     :   self.title,
            "codeName" : self.codeName,
            "baseUrl"   : self.baseUrl

        }
        return json.dumps(output, indent=3)



    def get_module_description(self):
        page = self.scrapper.get_page(self.baseUrl)
        soup = BSoup(page, "html.parser")
        description = soup.find("div", attrs={"class": "page-course"}).text
        return description

    def get_document_url(self):
        return None