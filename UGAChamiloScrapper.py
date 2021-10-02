import requests
import json
from UnofficialUGAChamiloAPI.IndexEngine import *
from UnofficialUGAChamiloAPI.Module import Module
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup as BSoup

DEFAULT_HEADERS_PATH    = "/data/headers.json"
DEFAULT_LOGINCAS_URL    = "https://chamilo.iut2.univ-grenoble-alpes.fr/main/auth/cas/logincas.php"
DEFAULT_TEST_URL        = "https://chamilo.iut2.univ-grenoble-alpes.fr/user_portal.php"
DEFAULT_MODULE_URL      = "https://chamilo.iut2.univ-grenoble-alpes.fr/user_portal.php"
DEFAULT_DOCUMENT_URL_FORMAT = "https://chamilo.iut2.univ-grenoble-alpes.fr/main/document/document.php?cidReq={}&id_session=0&gidReq=0&gradebook=0&origin="

def _load_json(filename):
    with open(filename, 'r') as file:
        data = json.loads(file.read())
    return data
def _log(text):
    print("[] " + text)
    None

class LoggedOutError(Exception):
    """Base class for exceptions in this module."""
    pass

class UGAChamiloScrapper:
    def __init__(
                    self,
                    credentials,
                    headers = None,
                    loginCasURL = DEFAULT_LOGINCAS_URL


                ):
        self.loginCasURL = loginCasURL
        self.baseHeaders = _load_json(DEFAULT_HEADERS_PATH) if headers == None else headers
        self.webSession = None
        self.credentials = credentials
        self.indexEngine = IndexEngine()
        self._reset_webSession()
        self.module_list = []

    def refresh(self):
        self._reset_webSession()
        self._sign_in()

    def get_credentials(self):
        return self.credentials

    def get_page(self, url):
        try:
            _log("Not logged out getting "+url)
            content = self._get_page(url).content
        except LoggedOutError:
            _log("logged out refreshing")
            self.refresh()
            content = self._get_page(url).content
        return content

    def _refresh_modules(self, modulePageUrl):
        modulePage = self.get_page(modulePageUrl)
        soup = BSoup(modulePage, "html.parser")
        moduleList = []
        for moduleElement in soup.find_all('h4', attrs={"class": "course-items-title"}):
            anchor = moduleElement.find('a')
            title = anchor.text.strip()
            moduleUrl = anchor["href"]
            nouveauModule = Module(self, title, moduleUrl, DEFAULT_DOCUMENT_URL_FORMAT)

            moduleList.append(nouveauModule)
        return moduleList

    def get_moduleList(self, modulePageUrl = DEFAULT_MODULE_URL):
        if len(self.module_list) == 0 :
            self.module_list = self._refresh_modules(modulePageUrl)
        return self.module_list

    def _sign_in(self):

        #Step one click on login button
        _log("login button click simulation")
        response = self._get_page(self.loginCasURL, check=False)
        casWebPage = response.content
        casUrl = response.url

        #Step two getting input fields value
        _log("getting from data from input fields")
        inputData = {}
        soup = BSoup(casWebPage, "html.parser")
        for input in soup.find_all("input"):
            inputData[input['name']] = input['value']

        #Step three entering password and username
        _log("writing username and password in form")
        inputData["username"] = self.get_credentials()["username"]
        inputData["password"] = self.get_credentials()["password"]

        #Step four submitting form
        _log("submitting form")
        response = self._post_page(casUrl, inputData, params=self.loginCasURL)

    def _is_session_valid(self, testUrl=DEFAULT_TEST_URL):
        _log("checking session")
        response = self._get_page(testUrl)
        return not "You are not allowed" in response.text

    def _reset_webSession(self):
        self.webSession = requests.Session()
        self.webSession.headers.update(self.baseHeaders)

    def _get_page(self, url, params=None, check=True):
        response = self.webSession.get(url, allow_redirects=True, params=params)
        badContentLength = [8987, 7824, 9074]
        if(check):
            response.headers["content-length"]
        if(check and int(response.headers["content-length"]) in badContentLength and "not allowed" in response.text):
            raise LoggedOutError

        return response

    def _post_page(self, url, data, params=None):
        return self.webSession.post(url,data=data,  allow_redirects=True, params=params)

    def add_folder_index_job(self, folder):

        return self.indexEngine.add_folder(folder)

    def start_index_engine(self):
        folderList = []
        for module in self.get_moduleList() :
            self.add_folder_index_job(module.get_rootFolder())
        self.indexEngine.run()

    def set_job_finished(self, job):
        self.indexEngine.remove_job_from_list(job)








