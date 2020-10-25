HOSE_DF_FN = "hose-2020_10_23-df.pickle"
ZIPPED_CLEANSED_DATA = "cleansedData-2020_10_23.zip"
import gdown
from common import exec3
import pickle

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