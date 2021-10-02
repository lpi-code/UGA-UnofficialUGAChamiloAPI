import json


class FunkyFile:
    def __init__(self,scrapper,  id, name, baseUrl):
        self.id = id
        self.name = name
        self.baseUrl = baseUrl
        self.scrapper = scrapper

    def _get_downloadUrl(self):

        return self.baseUrl + "&id=" + self.get_id()

    def download(self, savePath):
        path = savePath + '/' + self.name
        data = self.scrapper.get_page(self._get_downloadUrl())
        filemode = 'wb' if type(data) == bytes else 'w'
        with open(path, filemode) as file:
            file.write(data)

    def get_id(self):
        return self.id

    def get_identifier(self):
        output = {
            "id" : self.id,
            "name" : self.name

        }
        return output

