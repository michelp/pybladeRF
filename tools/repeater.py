import sys
import bladeRF
import threading

NULL  = bladeRF.ffi.NULL

@bladeRF.callback
def rx_callback(device, stream, meta_data,
                samples, num_samples, user_data):
    self = user_data
    with self.lock:
        with self.samples_available:
            if self.rx_idx < 0:
                return NULL
            ret = self.rx_stream.buffers[self.rx_idx]
            self.rx_idx += 1
            if self.rx_idx >= self.num_buffers:
                self.rx_idx = 0;

            if self.num_filled >= 2 * self.num_buffers:
                print "RX Overrun encountered. Terminating RX task."
                return NULL

            self.num_filled += 1
            self.samples_available.notify()
    return ret


@bladeRF.callback
def tx_callback(device, stream, meta_data,
                samples, num_samples, user_data):
    self = user_data
    with self.lock:
        if self.tx_idx < 0:
            return NULL

        if self.num_filled == 0:
            print "TX underrun encountered. Terminating TX task."
            return NULL
        ret = self.rx_stream.buffers[self.tx_idx]
        self.tx_idx += 1

        if self.tx_idx >= self.num_buffers:
            self.tx_idx = 0;

        self.num_filled -= 1
    return ret


class Repeater(object):

    def __init__(self, device_indentifier, config,
                 num_transfers=16,
                 samples_per_buffer=8192,
                 num_buffers=32):

        self.device = bladeRF.Device.from_params(device_indentifier, **config)

        self.rx_idx = 0
        self.tx_idx = 0
        self.num_filled = 0
        self.num_buffers = num_buffers
        self.prefill_count = num_transfers + (num_buffers - num_transfers) / 2
        self.lock = threading.Lock()
        self.samples_available = threading.Condition()

        self.rx_stream = self.device.rx.stream(
            rx_callback, num_buffers,
            bladeRF.FORMAT_SC16_Q12,
            samples_per_buffer, num_transfers, self)

        self.tx_stream = self.device.tx.stream(
            tx_callback,  num_buffers,
            bladeRF.FORMAT_SC16_Q12,
            samples_per_buffer, num_transfers, self)

    def run(self):
        self.rx_stream.start()
        with self.samples_available:
            while self.num_filled < self.prefill_count and self.tx_idx >= 0:
                self.samples_available.wait()

        self.tx_stream.start()
        i = raw_input('Repeater is running, press any key to exit... ')
        with self.lock:
            self.rx_idx = -1
            self.tx_idx = -1
        sys.exit(0)


if __name__ == '__main__':
    config = {
        # defaults for now
        }
    r = Repeater('', config)
    r.run()
