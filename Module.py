import json
from bs4 import BeautifulSoup as BSoup
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFolder import FunkyFolder

class Module :
    def __init__(self, parentScrapper, title,  baseUrl, documentUrlFormat):
        self.title = title
        self.codeName = baseUrl.split('/')[4]
        self.baseUrl = baseUrl
        self.scrapper = parentScrapper
        self.document_url = documentUrlFormat.format(self.codeName)
        self.rootFolder = FunkyFolder(self.scrapper, None, self.codeName, self.codeName, self.get_document_url())


    def get_rootFolder(self):
        return self.rootFolder
    def init_files(self):

        self.rootFolder.init_files()

    def dump(self):
        output = {
            "title"     :   self.title,
            "codeName"  : self.codeName,
            "baseUrl"   : self.baseUrl

        }
        return json.dumps(output, indent=3)



    def get_module_description(self):
        page = self.scrapper.get_page(self.baseUrl)
        soup = BSoup(page, "html.parser")
        description = soup.find("div", attrs={"class": "page-course"}).text
        return description

    def get_document_url(self ):
        return self.document_url

    def download(self, path):
        self.rootFolder.download(path)
        with open(path + "/" + self.codeName + "/" + "description.txt","w") as file:
            file.write(self.get_module_description())

    def get_funkyFileList(self):
        return self.rootFolder.get_funkyFileList()

    def get_rootFolder(self):
        return self.rootFolder