import neo
import numpy as np
from scipy import signal
from numpy import mean
import matplotlib.pyplot as plt


def emg_proc(emg):
    'Basic processing of raw EMG signal'

    emg['signal'] = emg['signal'] - mean(emg['signal'])
    nyq = emg['fs']/2
    low, high = 20/nyq, 500/nyq
    b, a = signal.butter(4, [low, high], btype='bandpass')
    emg['filt_signal'] = signal.filtfilt(b, a, emg['signal'], axis=0)
    emg['filt_rec_signal'] = abs(emg['filt_signal'])
    return emg


def tremor_proc(tremor):
    'Basic processing of tremor signal'

    nyq = tremor['fs']/2
    low = 30/nyq
    b, a = signal.butter(4, low, btype='lowpass')
    tremor['filt_signal'] = signal.filtfilt(b, a, tremor['signal'], axis=0)
    return tremor


def kinetic (flex, ext, angle, triangle):

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(angle['times'], angle['filt_signal'])
    plt.plot(triangle['times'], triangle['signal'])
    plt.subplot(2, 1, 2)
    plt.plot(ext['times'], ext['filt_rec_signal'])
    # Plot data with gain correction applied to flex
    plt.plot(flex['times'], -0.001*flex['filt_rec_signal'])


# create a reader
reader = neo.io.Spike2IO(filename='data.smr')
# read the block
bl = reader.read(cascade=True, lazy=False)[0]

flex = {}
ext = {}
angle = {}
triangle = {}
for i, asig in enumerate(bl.segments[0].analogsignals):
        times = asig.times.rescale('s').magnitude
        ch = str(asig.annotations['title']).split(sep="'")[1]
        fs = float(asig.sampling_rate)
        if ch == 'Flex':
            flex['times'] = times
            flex['signal'] = np.array(asig)
            flex['fs'] = fs
            flex = emg_proc(flex)
        elif ch == 'Ext':
            ext['times'] = times
            ext['signal'] = np.array(asig)
            ext['fs'] = fs
            ext = emg_proc(ext)
        elif ch == 'Angle':
            angle['times'] = times
            angle['signal'] = np.array(asig)
            angle['fs'] = fs
            angle = tremor_proc(angle)
        elif ch == 'triangle':
            triangle['times'] = times
            triangle['signal'] = np.array(asig)
            triangle['fs'] = fs

kinetic(flex, ext, angle, triangle)