from UnofficialUGAChamiloAPI.Engine.GenericEngine import GenericEngine
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFolder import *

from time import sleep


class IndexEngine(GenericEngine):
    def __init__(self, threadNb=40, batchSleepRatio=0.1):
        GenericEngine.__init__(self, FunkyFolder.init_files, threadNb, batchSleepRatio)

    def add_folder(self, folder):
        GenericEngine.add_job(self, folder.get_UUID(), folder)

    def remove_job_from_list(self, jobId):
        GenericEngine.done_job(self, jobId)

    def done_job(self, folder):
        GenericEngine.done_job(self, folder.get_UUID(), folder)
