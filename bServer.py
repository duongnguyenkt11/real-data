from bokeh.server.server import Server
from bokeh.application.handlers import FunctionHandler
from bokeh.util.browser import view
from common import *
from mufaseCommon import Tc, _module, My_module, initialize_port, threading_func_wrapper
from bokeh.models.widgets import Button, Slider, Div, DataTable, Paragraph
from bokeh.application.application import Application
from bokeh.plotting import figure
from bokeh.layouts import column, row, layout
import time
import bokeh

_module = My_module('bserver')
def pp(st):
    global _module
    return '%s%s%s'%(Tc.CGREEN2, st, Tc.CEND) + _module.banner()

#-----------------------------------------------------------------------------------------------------------------------
class Base_server:
    ALL_SERVERS = []

    @staticmethod
    def count_servers():
        print('There are ' + pp('%d server running')% len(Base_server.ALL_SERVERS))
        temp = '          Active ports: '; st = ''
        for s in Base_server.ALL_SERVERS: st += ('%d  '%s.port)
        if len(st) > 0: print(temp + pp(st))

    def wait_till_connected(self):
        while self.doc is None : pass

    def __init__(self, run=True, view=True, handler=None, l=None, name='Base_server0'):
        self.top = None; self.app = None; self.doc = None; self.fig = None
        self.layout = None
        # ----------------------------------
        def modify_doc(doc):
            p = figure(); p.circle([0, 5, 10], [0, 5, 10], size=15)
            self.top = column(p, Div(text='App has been created successfuly'))
            doc.add_root(self.top)
            pass
        #----------------------------------
        if handler is None: handler = modify_doc
        if l != None:
            self.l = l; handler = self.l.f
            l.attach_serv(self)
        self.port = initialize_port()
        self.app_handler = Application(FunctionHandler(handler))
        self.server = Server({'/' : self.app_handler}, num_proc=4, port=self.port, allow_websocket_origin = [f"*"])
        self.server.start()
        self.name=name; self.announce()
        Base_server.ALL_SERVERS.append(self)
        if run: self.start_ioloop()
        if view: self.server.io_loop.add_callback(lambda: self.go_to())

    pass #</__init__>

    def announce(self):
        print('%s successfully created '%self.name + _module.banner())

    def self_destroy(self):
        sessions = self.server.get_sessions()
        for sess in sessions:
            self.doc.destroy(sess)

    def get_tick_callbacks(self):
        return [cb for cb in self.doc.session_callbacks if type(cb) == bokeh.server.callbacks.NextTickCallback]

    def get_periodic_callbacks(self):
        return [cb for cb in self.doc.session_callbacks if type(cb) == bokeh.server.callbacks.PeriodicCallback]

    def remove_periodic(self):
        self.doc.remove_periodic_callback(self.get_periodic_callbacks()[0])

    def is_running(self):
        return self.server.io_loop.asyncio_loop.is_running()

    def start_ioloop(self):
        if self.is_running():
            print('Server %srunning already%s. Ignoring serv.start() request' % \
                 (Tc.CVIOLET2, Tc.CEND) + _module.banner())
        else: threading_func_wrapper(func=self.server.io_loop.start)

    def go_to(self, wait=False, show_time=True):
        t = time.time()
        count = len(self.server.get_sessions())
        view("http://localhost:%d/?bokeh-session-id=1" % self.port)
        if wait:
            while len(self.server.get_sessions()) == count: pass
            if show_time: print('time waited for connection: %.4f second(s)'%(time.time()-t))

    @staticmethod
    def show_timestamp():
        global _mod_bserver
        print('bserver object created ' +  str(_mod_bserver.banner()))
    #</Base_server>

#-----------------------------------------------------------------------------------------------------------------------
class Serv(Base_server): #Serv
    def __init__(self, handler = None, *args, **kwargs):
        super(Serv, self).__init__(handler=handler,*args, **kwargs)
#------------------------------------------------------------
# *** Main ***
_mod_bserver = My_module('bserver_module')

#%%

# The end