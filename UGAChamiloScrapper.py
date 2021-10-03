import requests
import logging
from UnofficialUGAChamiloAPI.Engine import IndexEngine, DownloadEngine
from UnofficialUGAChamiloAPI.Module import Module
from UnofficialUGAChamiloAPI.PagesOperations import *
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup as BSoup


DEFAULT_LOGINCAS_URL = "https://chamilo.iut2.univ-grenoble-alpes.fr/main/auth/cas/logincas.php"
DEFAULT_TEST_URL = "https://chamilo.iut2.univ-grenoble-alpes.fr/user_portal.php"
DEFAULT_MODULE_URL = "https://chamilo.iut2.univ-grenoble-alpes.fr/user_portal.php"
DEFAULT_DOCUMENT_URL_FORMAT = "https://chamilo.iut2.univ-grenoble-alpes.fr/main/document/document.php?cidReq={" \
                              "}&id_session=0&gidReq=0&gradebook=0&origin="


class LoggedOutError(Exception):
    pass

class SignInFailError(Exception):
    pass


class UGAChamiloScrapper:

    def __init__(
                self,
                credentials,
                headers=None,
                loginCasURL=DEFAULT_LOGINCAS_URL
                ):

        self.loginCasURL = loginCasURL
        self.baseHeaders = headers
        self.webSessions = []
        self.credentials = credentials
        self.module_list = []
        self.currentSessionIndex = 0
        self.nbSessions = 50
        for i in range(self.nbSessions):
            self.webSessions.append(requests.Session())

        #Initialising scrapping engine
        self.indexEngine = IndexEngine.IndexEngine()
        self.downloadEngine = DownloadEngine.DownloadEngine()



    def get_credentials(self):
        """
        Getter for credentials
        """
        return self.credentials

    def get_page(self, url):
        """
        Try to load a page (GET),
        if the account is disconnected, it automaticly refresh the session and log back in
        if the session is still not logged in : LoggedOutError will be raised
        """
        index = self._get_session_index()



        try:
            content = self._get_page(index, url).content


        except LoggedOutError:
            logging.warning("GET_PAGE : Logged out refreshing session")
            self.refresh_session(index)
            content = self._get_page(index, url).content
        logging.debug("GET_PAGE_DONE : {}".format(url))
        return content

    def get_moduleList(self, modulePageUrl=DEFAULT_MODULE_URL, forceRefresh=False):
        """
        Return module list (modules will be initialised if they are none or if refreshed is forced)
        """
        if len(self.module_list) == 0 or forceRefresh:
            self.module_list = self._refresh_modules(modulePageUrl)
        return self.module_list

    def refresh_session(self, index):
        """
        Clears the actual requests session and attemp to log back in
        """
        self._reset_webSession(index)
        self._sign_in(index)

    def add_folder_index_job(self, folder):

        return self.indexEngine.add_job(folder.get_UUID(), folder)

    def add_file_download_job(self, file, path):

        self.downloadEngine.add_job(file.get_UUID(),[file, path])



    def set_done_folder_index_job(self, folder):
        self.indexEngine.done_job(folder.get_UUID())

    def start_index_engine(self):
        folderList = []
        for module in self.get_moduleList():
            self.add_folder_index_job(module.get_rootFolder())
        self.indexEngine.run()

    def start_download_engine(self, path):
        for module in self.get_moduleList():
            self.add_file_download_job( module.get_rootFolder(), path )
        self.downloadEngine.run()

    def is_session_valid(self, index, testUrl=DEFAULT_TEST_URL):
        """
        Explicitly check if session is valid
        True if chamilo session is valid
        """
        logging.debug("MANUAL_SESSION_CHECK : checking session")
        try:
            response = self._get_page(index, testUrl)
            logging.debug("MANUAL_SESSION_CHECK : session valid")
            return True
        except LoggedOutError:
            return False
            logging.debug("MANUAL_SESSION_CHECK : session invalid")

    def _sign_in(self, index):
        """
        Key component : simulate user connection and the session will have the correct cookies
        """

        # Step one click on login button

        logging.debug("SIGN_IN : CHAMILO login button press simulation")
        response = self._get_page(index, self.loginCasURL, check=False)
        casWebPage = response.content
        casUrl = response.url

        # Step two getting input fields value
        logging.debug("SIGN_IN : CAS grabbing data from hidden inputFields")
        inputData = {}
        soup = BSoup(casWebPage, "html.parser")
        for input in soup.find_all("input"):
            inputData[input['name']] = input['value']

        # Step three entering password and username
        logging.debug("SIGN_IN : CAS completing form with credentials")
        inputData["username"] = self.get_credentials()["username"]
        inputData["password"] = self.get_credentials()["password"]

        # Step four submitting form
        logging.debug("SIGN_IN : CAS submit form")
        response = self._post_page(index, casUrl, inputData, params=self.loginCasURL)

        logging.debug("SIGN_IN : CHAMILO check session")
        if (self.is_session_valid(index)):
            logging.debug("SIGN_IN : CHAMILO session valid")
        else:
            logging.error("SIGN_IN : CHAMILO session invalid")
            raise(SignInFailError)
    def _reset_webSession(self, index):
        self.webSessions[index] = requests.Session()
        self.webSessions[index].headers.update(self.baseHeaders)


    def _get_page(self,index, url, params=None, check=True):
        response = self.webSessions[index].get(url, allow_redirects=True, params=params)

        if check and check_chamilo_login_state(response):
            raise LoggedOutError

        return response

    def _post_page(self,index, url, data, params=None):
        return self.webSessions[index].post(url, data=data, allow_redirects=True, params=params)

    def _refresh_modules(self, modulePageUrl):
        modulePage = self.get_page(modulePageUrl)
        soup = BSoup(modulePage, "html.parser")
        moduleList = []

        for moduleElement in soup.find_all('h4', attrs={"class": "course-items-title"}):

            anchor = moduleElement.find('a')
            if not anchor is None:
                title = anchor.text.strip()
                moduleUrl = anchor["href"]
                nouveauModule = Module(self, title, moduleUrl, DEFAULT_DOCUMENT_URL_FORMAT)

                moduleList.append(nouveauModule)
        return moduleList

    def _get_session_index(self):
        self.currentSessionIndex += 1
        if self.currentSessionIndex == self.nbSessions :
            self.currentSessionIndex = 0
        return self.currentSessionIndex



