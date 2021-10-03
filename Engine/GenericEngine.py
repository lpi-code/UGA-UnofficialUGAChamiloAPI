from concurrent.futures import ThreadPoolExecutor, wait
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFolder import *
import queue
from time import sleep

PENDING = "PENDING"
CURRENT = "CURRENT"
DONE = "DONE"


class jobNotFoundError(Exception):
    """Base class for exceptions in this module."""
    pass


class GenericEngine:
    def __init__(self, function, threadNb=40, batchSleepRatio=0.1, dynamicQueue=True):
        self.jobList = {
            PENDING: [],
            CURRENT: [],
            DONE: []

        }
        self.threadNb = threadNb
        self.batchSleepRatio = batchSleepRatio
        self.func = function
        self.dynamicQueue = dynamicQueue

    def run(self):
        with ThreadPoolExecutor(max_workers=self.threadNb) as executor:
            while self.get_nb_pending_job() > 0 or self.dynamicQueue and self.get_nb_current_job() > 0:
                while self.get_nb_pending_job():
                    jobArg = self._pop_job()
                    executor.submit(self.func, jobArg)
                sleep(self.batchSleepRatio * self.get_nb_current_job())

    def get_nb_pending_job(self):
        """
        Return number of pending job
        """

        return len(self.jobList[PENDING])

    def get_nb_current_job(self):
        """
        Return number of pending job
        """
        return len(self.jobList[CURRENT])

    def add_job(self, jobId, jobArguments):
        """
        Add Pending job
        """
        #print(self.dump_stats())
        #print("ENGINE : new job : {}".format(jobId))

        self.jobList[PENDING].append([jobId, jobArguments])

    def done_job(self, jobId):
        """
        Job is finished
        """
        self._move(jobId, CURRENT, DONE)

    def search_by_id(self, jobId, stackName):
        """
        Return index of job in stack or None
        """
        i = 0
        found = False

        while i < len(self.jobList[stackName]) and not found:
            found = (self.jobList[stackName][i][0] == jobId)
            i += 1
        return i - 1 if found else None

    def dump_stats(self):
        return "ENGINE : \tPending : {}\tCurrent : {}\tDone :{}".format(self.get_nb_pending_job(),
                                                                        self.get_nb_current_job(),
                                                                        len(self.jobList[DONE]))

    def _move(self, jobId, inputStack, outputStack):
        #print("ENGINE : Moving job : {} from  {} to {}".format(jobId, inputStack, outputStack))


        index = self.search_by_id(jobId, inputStack)
        if index is None:
            raise jobNotFoundError

        jobData = self.jobList[inputStack].pop(index)

        self.jobList[outputStack].append(jobData)
        print(self.dump_stats())
    def _pop_job(self):
        """
        Pop first pending job and return argument list
        """
        jobId = self.jobList[PENDING][0][0]
        arguments = self.jobList[PENDING][0][1]
        self._move(jobId, PENDING, CURRENT)
        return arguments
