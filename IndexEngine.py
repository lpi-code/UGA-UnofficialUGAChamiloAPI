from concurrent.futures import ThreadPoolExecutor, wait
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFolder import *
import queue
from time import sleep


class IndexEngine:
    def __init__(self, indexFunc=FunkyFolder.init_files):
        self.folderList = []
        self.running = False
        self.fileList=[]
        self.indexFunc = indexFunc
        self.jobList = []
    def run(self):

        self.running = True
        with  ThreadPoolExecutor(max_workers=30) as executor:
            while len(self.jobList) > 0:
                while(len(self.fileList) > 0):

                    executor.submit(self.indexFunc, self.fileList.pop(0))





    def add_folder(self, folder):
        self.jobList.append(folder._get_downloadUrl())
        self.fileList.append(folder)

    def remove_job_from_list(self, job):
        self.jobList.remove(job)
