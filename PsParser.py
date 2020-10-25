from common import *
from utilities import *
from CONSTANTS import *
from dataio import grabFiles
import json, os

DEBUG = True

class PsParser:
    def __init__(self, PATH=PARSER.PS_DATA_DIRECTORY):
        files = grabFiles(PATH, pattern="Phai")
        files = sorted([file for file in files if isValidTime(extractTime(file))])
        self.times = mmap(lambda file: extractTime(file),files)
        self.files = [os.path.join(PATH, file) for file in files]
        self.raw = mmap(self.parseFile, self.files)
        self.data = mmap(self.parseDataPoint, self.raw)
        if DEBUG: print(len(self.raw))

    @staticmethod
    def parseFile(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
        return data

    @staticmethod
    def parseDataPoint(d):
        buys  = mmap(lambda s: s.replace("ATC", PARSER.ATC_NUM_STR), d[0][1])
        sells = mmap(lambda s: s.replace("ATC", PARSER.ATC_NUM_STR), d[1][1])
        return mmap(lambda i: [int(buys[i][:-6]), float(buys[i][-6:])],
                    range(len(buys))), \
               mmap(lambda i: [int(sells[i][6:]), float(sells[i][:6])],
                    range(len(sells))),


p = PsParser()
#%%
p.data[0]


