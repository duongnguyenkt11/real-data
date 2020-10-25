from functools import reduce
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook
from CONSTANTS import *
from utilities import *
from bokeh.plotting import figure, output_file, show
import pandas as pd, numpy as np

ENVIRON = C.LOCAL

def mmap(*args):
    return list(map(*args))

class O:
    ################################################################################
    #                                    Init                                      #
    ################################################################################
    def __init__(self, cleansed, df=None):
        self.cleansed = cleansed
        self.n = len(cleansed[C.CTIME])
        self.hoseData = {cleansed[C.CTIME][i]: cleansed[C.CHOSE][i] for i in range(len(cleansed[C.CTIME]))}
        self.hoseArr = cleansed[C.CHOSE]
        self.stocks = sorted(list(cleansed[C.CHOSE][0].keys()))
        self.times = cleansed[C.CTIME]
        self.errorDataPoints = []

        self.hours = mmap(numerizeTime, self.times)
        self.seconds = mmap(toSeconds, self.times)
        self.Xs = mmap(numerizeTime, self.times)
        self.p = figure(plot_width=1400, plot_height=400)
        self.df = pd.DataFrame.from_dict(self.cleansed)

        self.nnBuyVolumes = [-1] * self.n
        self.nnSellVolumes = [-1] * self.n
        self.nnBuyValues = [-1] * self.n
        self.nnSellValues = [-1] * self.n

        self.numpied = False
        self.allPlots = []
        self.intervals = []
        self.totalLiquidity = []

    def numpyItUp(self):
        if self.numpied: return
        self.numpied = True
        a = [self.nnBuyVolumes, self.nnSellVolumes,  self.nnBuyValues, self.nnSellValues,
             self.hours, self.seconds, self.Xs, self.times]
        for x in a:
            x = np.array(x)


    ################################################################################
    #                               Utilities - Misc                               #
    ################################################################################

    def timeRange(self, start, end):
        resStart, resEnd = -1, -1
        for i in range(1, len(self.Xs)):
            if self.Xs[i] > start:
                resStart = i - 1
                break
        for i in range(len(self.Xs) - 1, 0, -1):
            if self.Xs[i] < end:
                resEnd = i + 1
                break
        return resStart, resEnd

    def setInterval(self, STEP=60):
        return


    ###############################################################################
    #                                  Computation                                #
    ###############################################################################

    def _calculateNNVolumes_i(self, i):
        time = self.times[i]
        print(f"\r{i}: {time}", end="")
        hose = self.hoseData[time]
        buys, sells = [], []
        try:
            buys = mmap(lambda stock: hose[stock][C.NN_BUY], self.stocks)
            sells = mmap(lambda stock: hose[stock][C.NN_SELL], self.stocks)
        except:
            self.errorDataPoints.append(time)
        finally:
            if len(buys) > 0 and len(sells) > 0:
                self.nnBuyVolumes[i] = buys
                self.nnSellVolumes[i] = sells

    def calculateNNVolumes(self):
        mmap(self._calculateNNVolumes_i, range(self.n))


    def _calculateNNValues_i(self, i):
        time = self.times[i]
        hose = self.hoseData[time]
        print(f"\r{i}: {time}", end="")
        self.nnBuyValues[i] = (reduce(lambda a, b: a + b,
                                      map(lambda stock: hose[stock][C.NN_BUY] * hose[stock][C.COL_AVG_PRICE], self.stocks)))
        self.nnSellValues[i] = (reduce(lambda a, b: a + b,
                                       map(lambda stock: hose[stock][C.NN_SELL] * hose[stock][C.COL_AVG_PRICE],
                                           self.stocks)))

    def calculateNNValues(self):
        mmap(self._calculateNNValues_i, range(self.n))

    def applyPricingConventions(self):
        self.nnBuyValues = [x / 100000 for x in self.nnBuyValues]
        self.nnSellValues = [x / 100000 for x in self.nnSellValues]

    def calculateTradedValues(self):
        def valAtSnapShot(time):
            hose = self.hoseData[time]
            stockTradedValue = lambda stock: hose[stock][C.COL_TOTAL_VOL]*hose[stock][C.COL_AVG_PRICE]
            vals = mmap(stockTradedValue, self.stocks)
            return reduce(lambda a, b: a + b, vals)
        self.totalLiquidity = mmap(valAtSnapShot, self.times)


    ################################################################################
    #                                      Plotting                                #
    ################################################################################

    def plot_Liquidity_Bar(self):
        return

    def initializePlot(self, file,p, ENVIRON=ENVIRON, title="HOSE"):
        if ENVIRON == C.LOCAL:
            output_file(file)
        else:
            output_notebook()
        if p is None:
            p = figure(plot_width=PC.WIDTH, plot_height=PC.HEIGHT, title=title)
            self.allPlots.append(p)
            return p
        return p


    def plot_BS_Pressure(self, p=None, file=FN.PLOT_BUY_SELL_PRESSURE_FILE):
        p = self.initializePlot(file, p, ENVIRON=ENVIRON, title="Ap luc mua, apluc ban")
        p.line(self.Xs, self.cleansed[C.CBUYP], line_width=2, color="green")
        p.line(self.Xs, self.cleansed[C.CSELLP], line_width=2, color="red")
        show(p)

    def plot_BS_Pressure2(self, p=None, file=FN.PLOT_BUY_SELL_PRESSURE_FILE):
        p = p = figure(plot_width=PC.WIDTH, plot_height=PC.HEIGHT, title="Apluc Mua Ban")
        p.line(self.Xs, self.cleansed[C.CBUYP], line_width=2, color="green")
        p.line(self.Xs, self.cleansed[C.CSELLP], line_width=2, color="red")
        return p


    def plot_NN_Liquidity_Bar(self, file="/home/sotola/foo.html", p=None):
        def prep(seconds, vals, STEP=20, REVERSED=False): # Prepare Data
            bins2 = []; x = [];bins, xs = intervalize(seconds, vals, STEP=STEP)
            for i in range(len(bins)):
                bins2.append(bins[i]); bins2.append(bins[i])
            for i in range(len(xs)):
                x.append(xs[i][0]); x.append(xs[i][1])
            if REVERSED: return x, [bin * -1 for bin in bins2]
            else: return x, bins2

        p = self.initializePlot(file, p, ENVIRON=ENVIRON, title="Thanh khoan khoi nuoc ngoai")
        xbuy, topbuy = prep(self.seconds, self.nnBuyValues)
        p.vbar(x=xbuy, top=toDelta(topbuy), width=0.01, color="green")
        xsell, topsell = prep(self.seconds, self.nnSellValues, REVERSED=True)
        p.vbar(x=xsell, top=toDelta(topsell), width=0.01, color="red")
        show(p)

    def plot__Liquidity_Bar(self, file="/home/sotola/Hose-MarketLiquidity.html", p=None):
        def prep(seconds, vals, STEP=20, REVERSED=False): # Prepare Data
            bins2 = []; x = [];bins, xs = intervalize(seconds, vals, STEP=STEP)
            for i in range(len(bins)):
                bins2.append(bins[i]); bins2.append(bins[i])
            for i in range(len(xs)):
                x.append(xs[i][0]); x.append(xs[i][1])
            if REVERSED: return x, [bin * -1 for bin in bins2]
            else: return x, bins2

        p = self.initializePlot(file, p, ENVIRON=ENVIRON, title="Thanh Khoan Thi Truong")
        xbuy, topbuy = prep(self.seconds, self.totalLiquidity)
        p.vbar(x=xbuy, top=toDelta(topbuy), width=0.01, color="green")
        show(p)


    def plot_NN_Accumulated_Values(self, p=None, file=FN.PLOT_NN_VALUES_FILE):
        p = self.initializePlot(file, p, ENVIRON=ENVIRON, title="Tong Thanh Khoan (NN)")
        p.line(self.Xs, np.array(self.nnBuyValues ) / 100000, line_width=2, color="green")
        p.line(self.Xs, np.array(self.nnSellValues) / 100000, line_width=2, color="red")
        show(p)

    def plot_NN_Velocity_Values(self, p=None, start=None, end=None, file=FN.PLOT_NN_VELOCITY_FILE):
        p = self.initializePlot(file, p, ENVIRON=ENVIRON)
        if not(start is None):
            start_i, end_i = self.timeRange(start, end)
        else:
            start_i = 0; end_i = -1

        buys = [x / 100000 for x in toDelta(self.nnBuyValues)[start_i:end_i]]
        sells = [x / 100000 for x in toDelta(self.nnSellValues)[start_i:end_i]]
        diffs = [buys[i] - sells[i] for i in range(len(sells))][start_i:end_i]
        p.line(self.Xs[start_i:end_i], buys, line_width=2, color="green")
        p.line(self.Xs[start_i:end_i], sells, line_width=2, color="red")
        show(p)




