from CONSTANTS import C, PC, FN
import pickle, numpy as np, pandas as pd
from dataio import loadCleansedData
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook
from copy import copy
from functools import reduce
from my_plots import myPlots
from testUtilities import *
from PsParser import PsParser
from dataio import *
from utilities import *
from O import O

class U:
    def __init__(self, times=None):
        self.name = "foo"
        self.times = loadToyData() if times is None else times
        self.seconds = mmap(toSeconds, self.times)

########################################################################################################################
#                                                           Main                                                       #
########################################################################################################################

u = U()

if __name__ == '__main__':
    def test_splitTerval():
        for i in range(3, len(u.seconds)):
            u.seconds[i] += 10000
        x = splitInterval(u.seconds[:100], DEBUG=True, returnIndex=True)

    test_splitTerval()

# cleansed = truncDataDict(o.cleansed, 3000, 6000)
# writePickle("/home/sotola/HOSE-3k-sample(2020-10-23).pickle")
#%%
#tik(); o = O(loadCleansedData()); tok()
tik(); o = O(loadSamplePrickle()); tok()
tik(); o.calculateNNVolumes(); tok();tik(); o.calculateNNValues(); tok();o.numpyItUp();o.calculateTradedValues()
_o = o

# o=O(_o.cleansed);tik(); o.calculateNNVolumes(); tok();tik(); o.calculateNNValues(); tok();o.numpyItUp()


o.plot_BS_Pressure(file="/home/sotola/graphs/ApLucMuaBan.html2.html")
o.plot_NN_Accumulated_Values(file="/home/sotola/graphs/NuocNgoaiLuyKe2.html")
o.plot_NN_Velocity_Values(file="/home/sotola/graphs/VelocityNuocNgoai2.html")
o.plot_NN_Liquidity_Bar(file="/home/sotola/graphs/ThanhKhoanNuocNgoai2.html")
o.plot__Liquidity_Bar(file="/home/sotola/graphs/ThanhKhoanThiTruong2.html")

#%%

########################################################################################################################
#                                                     PHAI SINH STUFF                                                  #
########################################################################################################################
p = PsParser()
x = 0
print("All Done!")


#%%
from bServer import *

from bokeh.io import show
from bokeh.models import Button, CustomJS



from bokeh.events import ButtonClick
from bokeh import model
def modify(doc):
    button = Button(label="Foo", button_type="success")

    def callback(event):
        print('Python:Click')

    button.on_event(ButtonClick, callback)
    doc.add_root(column(o.plot_BS_Pressure2(), button))

Base_server.show_timestamp()
serv = Serv(handler=modify,run=True, view=True)











