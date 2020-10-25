import sys, pandas as pd, bokeh
import threading
from bokeh.plotting import show, figure
from bokeh.models.widgets import Button, Slider, Div, DataTable, Paragraph
from bokeh.layouts import WidgetBox

from functools import reduce
from pyproj import Proj, transform


#%% 0. Misc
def write(st):
    if type(st) != str: st = str(st)
    sys.stdout.write(st+'\r')
    sys.stdout.flush()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def find_parent(doc, obj):
    id = obj.id
    if hasattr(doc, 'children'):
        for i in range(len(doc.children)):
            child = doc.children[i]
            if child.id == id:
                return doc, i
            else:
                res = find_parent(child, obj)
                if res is not None: return res
    return None

def tik():
    global _tik
    _tik = time.time()
    print('%sStarted%s '%(Tc.CVIOLET, Tc.CEND) + 'timing... at %s%s%s.'%
          (Tc.CBLACK, time_format(_tik, time_only=True), Tc.CEND))

def tok():
    global _tik
    print('Elapsed time: %s%.5f%s seconds' % (Tc.CVIOLET, time.time()-_tik, Tc.CEND) + _module.banner())




#%% 2.1



#%% 3. Coordinates projection & converts
def from_lng_lat(lng, lat):  # longitude first, latitude second.
    return transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), lng, lat)

def from_merc_xy(x, y):  # longitude first, latitude second.
    return transform(Proj(init='epsg:3857'), Proj(init='epsg:4326'), x, y)

def to_meter(lat1, lng1, lat2, lng2):
    from pyproj import Geod
    wgs84_geod = Geod(ellps='WGS84')
    az12, az21, dist = wgs84_geod.inv(lng1, lat1, lng2, lat2)
    return dist

def wgs84_to_web_mercator(df, lon="lon", lat="lat"):
    import numpy as np
    import warnings
    warnings.simplefilter('ignore')
    """Converts decimal longitude/latitude to Web Mercator format"""
    k = 6378137
    df["x"] = df[lon] * (k * np.pi/180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
    return df

#%% 4. Timestamp_utilities
import time

def time_format(t, time_only=False):
    st = time.strftime('%Y/%m/%d  %I:%M:%S %p',time.localtime(t))
    if time_only: st = st[-11:-3]
    return st

#%% 5. Ansi colors
class Tc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    CGREYBG = '\33[100m'
    CREDBG2 = '\33[101m'
    CGREENBG2 = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2 = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2 = '\33[106m'
    CWHITEBG2 = '\33[107m'

class Tc2:
    SOURCE_ANSI_COLOR = Tc.CEND
    TIME_ANSI_COLOR = Tc.CEND
    INCIDENT_ANSI_COLOR = Tc.CEND
    LOCATION_ANSI_COLOR = Tc.CEND
    OPERATOR_ANSI_COLOR = Tc.CEND
    OPERATOR_TICKET_COUNT = Tc.CEND
    TICKET_ID_ANSI_COLOR = Tc.CEND
    TICKET_COUNT_ANSI_COLOR = Tc.CEND

#%% 6. Threading function wrapper
def threading_func_wrapper(func, delay=0.5, args=None, start=True):
    if args is None:
        func_thread = threading.Timer(delay, func)
    else:
        func_thread = threading.Timer(delay, func, (args,))
    if start: func_thread.start()
    return func_thread

#%% *** Module banner ***
class My_module:
    def __init__(self, module_name,  compile_time=None, pprint=False):
        if compile_time is None: compile_time = time.time()
        self.compile_time = compile_time
        self.module_name = module_name

    def banner(self):
        return ' (msg from %s%s%s.py compiled at %s%s%s)' % \
               (Tc.CYELLOW, self.module_name, Tc.CEND,
                Tc.CBLACK, time_format(self.compile_time)[-11:-3],Tc.CEND)

    def __repr__(self):
        return '***%s%s%s*** compiled at %s' % \
               (Tc.CYELLOW, self.module_name, Tc.CEND,
                time_format(self.compile_time))

#%% 8.Bokeh server port caching
def initialize_port():
    global _count
    BOKEH_PORT = 5010;
    BOKEH_PORT_FILE = '/home/sotola/current_bokeh_port.txt'
    with open(BOKEH_PORT_FILE, 'r+') as file: _count = file.read()
    _count = int(_count) + 1
    if _count > 5200: _count = 5001
    with open(BOKEH_PORT_FILE, 'w+') as file: file.write(str(_count))
    return _count

#%% Module_level variables

_module = My_module('common')

#%% *** main ***
if __name__ == '__main__':
    global mody
    mody = My_module('__main__.has_ben_run() == True')
    print(mody)
