HOSE_DF_FN = "hose-2020_10_23-df.pickle"
ZIPPED_CLEANSED_DATA = "cleansedData-2020_10_23.zip"
import gdown
from  CONSTANTS import PARSER
from utilities import *
from common import exec3
import pickle
from  functools import reduce


# gdown.download("https://drive.google.com/uc?id=1E_DvlRW7Awc-BeTh2oUQ9yQJ8_vfBZ5r", ZIPPED_CLEANSED_DATA, quiet=False)
# exec3(f"unzip -o {ZIPPED_CLEANSED_DATA}")

def loadCleansedData(CLEANSED_DATA=HOSE_DF_FN):
  with open(HOSE_DF_FN, 'rb') as myFile:
    import pickle
    df = pickle.load(myFile)
  return df

def loadToyData(FILE_NAME="/home/sotola/times.pickle"):
    with open(FILE_NAME, "rb")as file:
      return pickle.load(file)

def writePickle(obj, FILE_NAME="/home/sotola/quickSave.pickle"):
    with open(FILE_NAME, "wb") as file:
      pickle.dump(obj, file)

def loadSamplePrickle(FILE_NAME="/home/sotola/HOSE-3k-sample(2020-10-23).pickle"):
    with open(FILE_NAME, "rb") as file:
      return pickle.load(file)


#%%

def readFile(fp):
    import json
    with open(fp, "r") as file:
        data = json.loads(file.read())
    return data

def parsePrice(x):
    if x.replace(".", "").isnumeric(): return float(x)
    return 0

def parseVol(x):
    x = x.replace(",", "")
    if x.isnumeric(): return int(x) * 10
    return 0

def parseHose(data):
    dic = {}
    def parseRow(row):
        raw = row[1:]
        raw[C.COL_GIA1] = parsePrice(raw[C.COL_GIA1])
        raw[C.COL_GIA2] = parsePrice(raw[C.COL_GIA2])
        raw[C.COL_GIA3] = parsePrice(raw[C.COL_GIA3])
        raw[C.COL_VOL1] = parseVol(raw[C.COL_VOL1])
        raw[C.COL_VOL2] = parseVol(raw[C.COL_VOL2])
        raw[C.COL_VOL3] = parseVol(raw[C.COL_VOL3])
        raw[C.COL_GIA1b] = parsePrice(raw[C.COL_GIA1b])
        raw[C.COL_GIA2b] = parsePrice(raw[C.COL_GIA2b])
        raw[C.COL_GIA3b] = parsePrice(raw[C.COL_GIA3b])
        raw[C.COL_VOL1b] = parseVol(raw[C.COL_VOL1b])
        raw[C.COL_VOL2b] = parseVol(raw[C.COL_VOL2b])
        raw[C.COL_VOL3b] = parseVol(raw[C.COL_VOL3b])
        raw[C.COL_GIA] = parseVol(raw[C.COL_GIA])
        raw[C.COL_VOL] = parseVol(raw[C.COL_VOL])
        raw[C.COL_TOTAL_VOL] = parseVol(raw[C.COL_TOTAL_VOL])
        raw[C.COL_AVG_PRICE] = parsePrice(raw[C.COL_AVG_PRICE])
        raw[C.COL_HIGH] = parsePrice(raw[C.COL_HIGH])
        raw[C.COL_LOW] = parsePrice(raw[C.COL_LOW])
        raw[C.NN_SELL] = parseVol(raw[C.NN_SELL])
        raw[C.NN_BUY] = parseVol(raw[C.NN_BUY])

        dic[row[0]] = raw
    mmap(parseRow, data)
    return dic

def mmap(*args):
    return list(map(*args))

def extractTime(file):
    timeString = file[file.find("2020") + 4:file.find(".json")]
    hour, minute, second = mmap(int, timeString.split("_"))
    if len(timeString) == len("9_59_59"):
        timeString = "0" + timeString
    return timeString

def buyPressure(hose):
    def stockBuyPressure(stock):
        data = hose[stock]
        return data[C.COL_VOL1] * data[C.COL_GIA1] + data[C.COL_VOL2] * data[C.COL_GIA2] + data[C.COL_VOL3] * data[C.COL_GIA3]
    return reduce(lambda a, b: a + b, map(stockBuyPressure, hose))

def sellPressure(hose):
    def stockSellPressure(stock):
        data = hose[stock]
        return data[C.COL_VOL1b] * data[C.COL_GIA1b] + data[C.COL_VOL2b] * data[C.COL_GIA2b] + data[C.COL_VOL3b] * data[C.COL_GIA3b]
    return reduce(lambda a, b: a + b, map(stockSellPressure, hose))

def beautify(x, num_decimal=2):
  if num_decimal==2: return float(f"{x:.2f}")
  if num_decimal==3: return float(f"{x:.3f}")
  if num_decimal==4: return float(f"{x:.4f}")
  if num_decimal==5: return float(f"{x:.5f}")
  if num_decimal==6: return float(f"{x:.6f}")

def isValidTime(time):
  if "09_00_00" <= time <= "11_30_00": return True
  if "13_00_00" <= time <= "13_30_00": return True
  return False

#%%
import os

def grabFile(st = ""):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(PARSER.PS_DATA_DIRECTORY) if (
            isfile(join(PARSER.PS_DATA_DIRECTORY, f)) &
            f.__contains__(st) & (not f.__contains__("(")))]
    return onlyfiles

files = grabFile("Phai")

files = sorted([file for file in files if isValidTime(extractTime(file))])
len(files)

#%%













