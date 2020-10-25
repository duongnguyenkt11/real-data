################################################################################
#                                Declare  Constants                            #
################################################################################
class C:
    COL_GIA3 = 3
    COL_VOL3 = 4
    COL_GIA2 = 5
    COL_VOL2 = 6
    COL_GIA1 = 7
    COL_VOL1 = 8

    COL_GIA = 9
    COL_VOL = 10

    COL_GIA1b = 12
    COL_VOL1b = 13
    COL_GIA2b = 14
    COL_VOL2b = 15
    COL_GIA3b = 16
    COL_VOL3b = 17
    COL_TOTAL_VOL = 18
    COL_AVG_PRICE = 21
    COL_HIGH = 22
    COL_LOW = 23
    NN_BUY = 24
    NN_SELL = 25

    DATA_2_PLOT_RATIO = 100000

    CTIME = "times"
    CBUYP = "buyPressure"
    CSELLP = "sellPressure"
    CHOSE="hoseSnapShot"
    LOCAL="local"

class PC: # plot constants
    WIDTH = 1000
    HEIGHT = 400

class FN:
    PLOT_NN_VALUES_FILE="/home/sotola/NuocNgoaiLuyKe.html"
    PLOT_NN_VELOCITY_FILE = "/home/sotola/NuocNgoaiVelocity.html"
    PLOT_BUY_SELL_PRESSURE_FILE = "/home/sotola/ApLucMuaBan.html"

class KEYS:
    TIMES='times'
    HOSE_SNAPSHOT = 'hoseSnapShot'
    BUY_PRESSURE  = 'buyPressure'
    SELL_PRESSURE = 'sellPressure'
