from __future__ import division
import sys
import threading
from Queue import Queue

import matplotlib.animation as animation
from matplotlib.mlab import psd
import pylab as pyl
import numpy as np

import bladeRF


@bladeRF.callback
def rx_callback(device, stream, meta_data,
                samples, num_samples, user_data):
    self = user_data

    with self.lock:
        if self.rx_idx < 0:
            return

        ret = self.rx_stream.buffers[self.rx_idx]
        self.sample_q.put(bladeRF.samples_to_floats(ret, num_samples))

        self.rx_idx += 1
        if self.rx_idx >= self.num_buffers:
            self.rx_idx = 0

        return ret


NFFT = 1024*4
NUM_SAMPLES_PER_SCAN = NFFT*16
NUM_BUFFERED_SWEEPS = 100

NUM_SCANS_PER_SWEEP = 1

FREQ_INC_COARSE = 1e6
FREQ_INC_FINE = 0.1e6
GAIN_INC = 5


class Waterfall(object):

    def __init__(self, device_indentifier, config,
                 num_transfers=16,
                 samples_per_buffer=1024,
                 num_buffers=32):

        self.image_buffer = -100*np.ones((NUM_BUFFERED_SWEEPS,
                                          NUM_SCANS_PER_SWEEP*NFFT))
        self.keyboard_buffer = []
        self.shift_key_down = False
        self.fig = pyl.figure()
        self.lock = threading.Lock()
        self.device = bladeRF.Device.from_params(device_indentifier, **config)
        self.sample_q = Queue()

        self.rx_idx = 0
        self.num_buffers = num_buffers

        self.rx_stream = self.device.rx.stream(
            rx_callback, num_buffers,
            bladeRF.FORMAT_SC16_Q12,
            samples_per_buffer, num_transfers, self)

        self.ax = self.fig.add_subplot(1,1,1)
        self.image = self.ax.imshow(self.image_buffer, aspect='auto',\
                                    interpolation='nearest', vmin=-50, vmax=10)
        self.ax.set_xlabel('Current frequency (MHz)')
        self.ax.get_yaxis().set_visible(False)

        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)

    def run(self):
        self.rx_stream.start()
        self.update_plot_labels()
        ani = animation.FuncAnimation(self.fig, self.update, interval=50,
                blit=True)
        pyl.show()
        with self.lock:
            self.rx_idx = -1
        sys.exit(0)

    def update_plot_labels(self):
        fc = self.device.rx.frequency
        rs = self.device.rx.sample_rate
        freq_range = (fc - rs/2)/1e6, (fc + rs*(NUM_SCANS_PER_SWEEP - 0.5))/1e6

        self.image.set_extent(freq_range + (0, 1))
        self.fig.canvas.draw_idle()

    def on_scroll(self, event):
        if event.button == 'up':
            self.device.rx.frequency += FREQ_INC_FINE if self.shift_key_down else FREQ_INC_COARSE
            self.update_plot_labels()
        elif event.button == 'down':
            self.device.rx.frequency -= FREQ_INC_FINE if self.shift_key_down else FREQ_INC_COARSE
            self.update_plot_labels()

    def on_key_press(self, event):
        if event.key == '+':
            self.sdr.gain += GAIN_INC
        elif event.key == '-':
            self.sdr.gain -= GAIN_INC
        elif event.key == ' ':
            self.sdr.gain = 'auto'
        elif event.key == 'shift':
            self.shift_key_down = True
        elif event.key == 'right':
            self.device.rx.frequency += FREQ_INC_FINE if self.shift_key_down else FREQ_INC_COARSE
            self.update_plot_labels()
        elif event.key == 'left':
            self.device.rx.frequency -= FREQ_INC_FINE if self.shift_key_down else FREQ_INC_COARSE
            self.update_plot_labels()
        elif event.key == 'enter':
            # see if valid frequency was entered, then change center frequency
            try:
                # join individual key presses into a string
                input = ''.join(self.keyboard_buffer)

                # if we're doing multiple adjacent scans, we need to figure out
                # the appropriate center freq for the leftmost scan
                center_freq = float(input)*1e6 + (self.device.rx.sample_rate/2)*(1 - NUM_SCANS_PER_SWEEP)
                self.device.rx.frequency = center_freq

                self.update_plot_labels()
            except ValueError:
                pass

            self.keyboard_buffer = []
        else:
            self.keyboard_buffer.append(event.key)

    def on_key_release(self, event):
        if event.key == 'shift':
            self.shift_key_down = False

    def update(self, *args):
        # save center freq. since we're gonna be changing it
        start_fc = self.device.rx.frequency

        # prepare space in buffer
        # TODO: use indexing to avoid recreating buffer each time
        self.image_buffer = np.roll(self.image_buffer, 1, axis=0)

        for scan_num, start_ind in enumerate(range(0, NUM_SCANS_PER_SWEEP*NFFT, NFFT)):
            self.device.rx.frequency += self.device.rx.sample_rate*scan_num

            # estimate PSD for one scan
            samples = np.frombuffer(bladeRF.ffi.buffer(self.sample_q.get(), NUM_SAMPLES_PER_SCAN*8), np.complex64)
            psd_scan, f = psd(samples, NFFT=NFFT)

            self.image_buffer[0, start_ind: start_ind+NFFT] = 10*np.log10(psd_scan)

        # plot entire sweep
        self.image.set_array(self.image_buffer)

        # restore original center freq.
        self.device.rx.frequency = start_fc

        return self.image,


if __name__ == '__main__':
    config = {
        'rx_frequency': 440000000,
        }
    r = Waterfall('', config)
    r.run()
