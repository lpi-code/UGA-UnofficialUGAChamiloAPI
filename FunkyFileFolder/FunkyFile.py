import json


class FunkyFile:
    def __init__(self, scrapper, id, name, moduleName, baseUrl):
        self.id = id
        self.name = ""
        self.set_name(name)
        self.baseUrl = baseUrl
        self.scrapper = scrapper
        self.moduleName = moduleName

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
            "id": self.id,
            "name": self.name

        }
        return output

    def get_UUID(self):
        return self.moduleName + "_" + str(self.get_id())

    def _get_downloadUrl(self):
        return self.baseUrl + "&id=" + self.get_id()

    def set_name(self, name):
        name = name.strip()
        unwantedChars = [":", "/", "\\", "'", "\"", "%", "(", ")", "{", "}", "-"]
        for car in unwantedChars:
            name = name.replace(car, "_")
        self.name = name

    def get_name(self, name):
        return self.name

    def get_moduleName(self):
        return self.moduleName