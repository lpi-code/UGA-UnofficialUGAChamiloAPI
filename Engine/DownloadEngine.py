from UnofficialUGAChamiloAPI.Engine.GenericEngine import GenericEngine
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFolder import *
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFile import *

from time import sleep


class DownloadEngine(GenericEngine):
    def __init__(self, threadNb=100, batchSleepRatio=0.1):
        GenericEngine.__init__(self, self.download_func, threadNb, batchSleepRatio)

    def download_func(self, args):
        """
        arg = [ file , path ]
        """

        args[0].download(args[1])

        self.done_job(args[0].get_UUID())

    def add_file(self, file, path):
        GenericEngine.add_job(self, file.get_UUID(), [file,path])

