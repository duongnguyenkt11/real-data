from copy import copy
from functools import reduce
from CONSTANTS import C, PC, FN

def mmap(*args):
    return list(map(*args))

def numerizeTime(st):
    a = st.split("_")
    return (int(a[0]) * 3600 + int(a[1]) * 60 + int(a[2])) / 3600

def toDelta(values):
    lst = [0] * len(values)
    for i in range(1, len(lst)):
        lst[i] = values[i] - values[i - 1]
    return lst

def findLastMorning(times):
  for i in range(len(times)):
    if times[i] <= "11_30_00" < times[i + 1]:
      return times[i], i
  return times[0]

def findFirstAfternoon(times):
  for i in range(1, len(times)):
    if times[i - 1] < "13_00_00" <= times[i]:
      return times[i], i
  return times[0]

def toSeconds(time):
  res = 0
  a = mmap(int, time.split("_"))
  return a[0]*3600 + a[1]*60 + a[2]

def toSeconds(time):
  res = 0
  a = mmap(int, time.split("_"))
  return a[0]*3600 + a[1]*60 + a[2]

#interval
def splitInterval(a, STEP=20, PAD=0.49999999, DEBUG=False, returnIndex=False):
    res = []; current = []
    n = len(a)
    assert n > 2, f"error calling splitInterval({a}, {STEP})"
    start = a[0] - PAD; next = start + STEP; end = a[-1] + PAD
    if DEBUG: print(f"[{start:.1f}:{next:.1f} ==> ", end="")

    for i in range(n + 1):
        if i > n - 1:
            if DEBUG: print("] \nAll done!")
            res.append(copy(current))
            break

        if a[i] > next:                 # Build a new interval
            start = a[i] - PAD
            next = start + STEP
            if DEBUG: print("]")
            res.append(copy(current))
            current = []
            if DEBUG: print(f"[{start:.1f}:{next:.1f} ==> ", end="")

        current.append(i if returnIndex  else a[i])
        if DEBUG: print(f"{current[-1]} ", end="")
    assert reduce(lambda a, b: a + b, map(len, res)) == len(a), "Error calling splitInterval! Missing values"
    return res

def tok():
    import time
    CEND = '\33[0m'; CVIOLET = '\33[35m'
    global _time
    print(f"Elapsed time: {CVIOLET}{round(time.time() - _time, 2)}{CEND} seconds. "
          f"({time_format(time_only=True)})")

def tik(verbose=False):
    import time
    global _time
    _time = time. time()
    CEND = '\33[0m'; CVIOLET = '\33[35m'
    if verbose:
        print(f"Started timing: {CVIOLET}{time_format(time_only=True)}{CEND}.")

def time_format(t=-1, time_only=False, adjust = 7):
    import time
    if t == -1: t = time.time()
    st = time.strftime('%Y/%m/%d  %I:%M:%S %p',time.localtime(t + 3600* adjust))
    if time_only: st = st[-11:]
    return st

def truncDataDict(source, start=0, end=-1):
    d = {}
    def process(key):
        d[key] = source[key][start:end]

    mmap(process, source.keys())
    return d

def myMax(indices, values):
    m = -200000000000000
    for i in indices:
        if m < values[i]/C.DATA_2_PLOT_RATIO: m = values[i]/C.DATA_2_PLOT_RATIO
        # print(f" max: {values[i]}",end="")
    return m

def beautify(num, numDecimal=2, returnNumber=True):
    if numDecimal == 1: s = f"{num:.1f}"
    else:
        if numDecimal == 2: s = f"{num:.2f}"
        else:
            if numDecimal == 3: s = f"{num:.3f}"
            else: s = f"{num:.4f}"
    if not returnNumber: return s
    return float(s)

def representInterval(interval, seconds):
    if len(interval) < 2:
        print(seconds[interval[0]]/3600)
        return seconds[interval[0]]/3600, seconds[interval[0]]/3600
    else:
        return seconds[interval[0]]/3600, seconds[interval[-1]]/3600

def intervalize(seconds, vals, STEP=10, intervals=None, accumulatorFunction=myMax, beautiful=True):
    if intervals is None:
        intervals = splitInterval(seconds, STEP=STEP, returnIndex=True)
    bins = mmap(lambda indices: myMax(indices, vals), intervals)
    if beautiful: bins = mmap(lambda x: beautify(x, numDecimal=2), bins)
    return bins, mmap(lambda x: representInterval(x, seconds), intervals)