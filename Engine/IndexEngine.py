from UnofficialUGAChamiloAPI.Engine.GenericEngine import GenericEngine
from UnofficialUGAChamiloAPI.FunkyFileFolder.FunkyFolder import *

from time import sleep


class IndexEngine(GenericEngine):
    def __init__(self, threadNb=40, batchSleepRatio=0.1):
        GenericEngine.__init__(self, FunkyFolder.init_files, threadNb, batchSleepRatio)





