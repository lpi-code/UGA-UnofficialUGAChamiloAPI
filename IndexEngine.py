from concurrent.futures import ThreadPoolExecutor, wait
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFolder import *
import queue
from time import sleep


class IndexEngine:
    def __init__(self, indexFunc=FunkyFolder.init_files, threadNb=40, batchSleepRatio=0.1):
        self.folderList = []
        self.running = False
        self.fileList=[]
        self.indexFunc = indexFunc
        self.jobList = []
        self.threadNb = threadNb
        self.batchSleepRatio = batchSleepRatio
    def run(self):

        self.running = True
        with  ThreadPoolExecutor(max_workers=self.threadNb) as executor:
            while len(self.jobList) > 0:
                while(len(self.fileList) > 0):

                    executor.submit(self.indexFunc, self.fileList.pop(0))
                sleep(self.batchSleepRatio*len(self.jobList))


    def add_folder(self, folder):
        self.jobList.append(folder.get_UUID())
        self.fileList.append(folder)

    def remove_job_from_list(self, job):
        self.jobList.remove(job)
