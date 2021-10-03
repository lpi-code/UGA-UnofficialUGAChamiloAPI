from UnofficialUGAChamiloAPI.Engine.GenericEngine import GenericEngine
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFolder import *
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFile import *

from time import sleep


class DownloadEngine(GenericEngine):
    def __init__(self, threadNb=3, batchSleepRatio=0.1):
        GenericEngine.__init__(self, self.download_func, threadNb, batchSleepRatio)

    def download_func(self, args):
        """
        arg = [ file , path ]
        """
        print("DOWNLOAD ENGINE : downloading " + args[0].get_UUID() + " in " + args[1])
        args[0].download(args[1])

    def add_file(self, file, path):
        GenericEngine.add_job(self, file.get_UUID(), [file,path])

    def remove_job_from_list(self, jobId):
        GenericEngine.done_job(self, jobId)
