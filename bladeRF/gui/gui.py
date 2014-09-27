import pyqtgraph as pg
import Queue
from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal, Qt
import scipy.ndimage as ndi
import numpy as np

app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

from scipy import signal
import bladeRF

device = bladeRF.Device()
device.rx.enabled = True
device.rx.frequency = 440000000
device.rx.bandwidth = 28000000
device.rx.sample_rate = 40000000



num_buffers = 16
num_transfers = 16
num_samples = 2**16
Nf = 512     # No. of frames
Ns = 1000    # Signal length

params = [
    {'name': 'Frequency',
     'type': 'group',
     'children': [
         {'name': 'Mhz',
          'type': 'int',
          'decimals': 12,
          'value': device.rx.frequency,
      },
     ]},

    {'name': 'Bandwidth',
     'type': 'group',
     'children': [
         {
             'name': 'Mhz',
             'type': 'int',
             'value': device.rx.bandwidth,
             'step': 1,
             'dec': True,
         },
     ]},
    
    {'name': 'Sample Rate', 'type': 'group', 'children': [
        {'name': 'Mhz',
         'type': 'int',
         'value': device.rx.sample_rate},
    ]},

    {'name': 'Gain', 'type': 'group', 'children': [
        {'name': 'LNA', 'type': 'list',
         'values': {
             "mid": bladeRF.LNA_GAIN_MID,
             "max": bladeRF.LNA_GAIN_MAX,
             "bypass": bladeRF.LNA_GAIN_BYPASS
         },
         'value': bladeRF.LNA_GAIN_MAX},

        {'name': 'VGA1',
         'type': 'int',
         'limits': (5, 30),
         'value': device.rx.vga1},

        {'name': 'VGA2',
         'type': 'int',
         'limits': (0, 30),
         'value': device.rx.vga2},
    ]},
]

## Create tree of Parameter objects
p = Parameter.create(name='params', type='group', children=params)

## If anything changes in the tree, print a message
def change(param, changes):
    for param, change, data in changes:
        path = p.childPath(param)
        if path is not None:
            childName = '.'.join(path)
        else:
            childName = param.name()
        if childName.startswith('Frequency'):
            device.rx.frequency = data
        elif childName.startswith('Bandwidth'):
            device.rx.bandwidth = data
        elif childName.startswith('Sample Rate'):
            device.rx.sample_rate = data
        elif childName.startswith('Gain.LNA'):
            device.rx.lna_gain = data
        elif childName.startswith('Gain.VGA1'):
            device.rx.vga1 = data
        elif childName.startswith('Gain.VGA2'):
            device.rx.vga2 = data

    
p.sigTreeStateChanged.connect(change)

## Create two ParameterTree widgets, both accessing the same data
t = ParameterTree()
t.setParameters(p, showTop=False)
t.setWindowTitle('pyqtgraph example: Parameter Tree')
t2 = ParameterTree()
t2.setParameters(p, showTop=False)

win = QtGui.QWidget()

layout = QtGui.QGridLayout()
win.setLayout(layout)

Arx = np.zeros([Nf, Ns])
inwin = pg.ImageView(view=pg.PlotItem())
inwin.setImage(Arx, scale=[2, 2])

queue = Queue.Queue(num_buffers)

def update():
    global Arx
    Arx = np.roll(Arx, 1, axis=0)
    try:
        samples = queue.get_nowait()
    except Queue.Empty:
        return
    f, fft = signal.periodogram(samples, window='hamming', scaling='density', nfft=Ns)
    fft = 10*np.log10(fft)
    Arx[0] = fft
    inwin.setImage(Arx.T, autoRange=False, scale=[2, 2])

layout.addWidget(inwin, 1, 0, 1, 10)

#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
inwin.addItem(vLine, ignoreBounds=True)
inwin.addItem(hLine, ignoreBounds=True)

def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if inwin.imageItem.sceneBoundingRect().contains(pos):
        mousePoint = inwin.imageItem.getViewBox().mapSceneToView(pos)
        index = int(mousePoint.x())
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())

proxy = pg.SignalProxy(inwin.scene.sigMouseMoved, rateLimit=60, slot=mouseMoved)


layout.addWidget(QtGui.QLabel(
    "BladeRF spectrum."), 0,  0, 1, 2)
layout.addWidget(t, 1, 11, 1, 3)

win.show()
win.resize(1600,800)

def rx(device, stream, meta_data, samples, num_samples, user_data):
    samples = bladeRF.samples_to_narray(samples, num_samples)
    try:
        queue.put_nowait(samples)
    except Queue.Full:
        pass
    return stream.next()

stream = device.rx.stream(
    rx,
    num_buffers,
    bladeRF.FORMAT_SC16_Q12,
    num_samples,
    num_transfers,
)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start()
stream.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        stream.running = False
        stream.join()
