import sys
import bladeRF
import threading


@bladeRF.callback
def rx_callback(device, stream, meta_data, samples, num_samples, repeater):
    with repeater.samples_available:
        if repeater.rx_idx < 0:
            return
        ret = repeater.rx_stream.buffers[repeater.rx_idx]
        repeater.rx_idx += 1
        if repeater.rx_idx >= repeater.num_buffers:
            repeater.rx_idx = 0
        if repeater.num_filled >= 2 * repeater.num_buffers:
            print "RX Overrun encountered. Terminating RX task."
            return
        repeater.num_filled += 1
        repeater.samples_available.notify()
    return ret


@bladeRF.callback
def tx_callback(device, stream, meta_data, samples, num_samples, repeater):
    with repeater.samples_available:
        if repeater.tx_idx < 0:
            return
        if repeater.num_filled == 0:
            print "TX underrun encountered. Terminating TX task."
            return
        ret = repeater.rx_stream.buffers[repeater.tx_idx]
        repeater.tx_idx += 1
        if repeater.tx_idx >= repeater.num_buffers:
            repeater.tx_idx = 0
        repeater.num_filled -= 1
    return ret


class Repeater(object):

    def __init__(self, device_indentifier, config, num_transfers=16,
                 samples_per_buffer=8192, num_buffers=32):

        self.device = bladeRF.Device.from_params(device_indentifier, **config)
        self.rx_idx = self.tx_idx = self.num_filled = 0
        self.num_buffers = num_buffers
        self.prefill_count = num_transfers + (num_buffers - num_transfers) / 2
        self.samples_available = threading.Condition()

        self.rx_stream = self.device.rx.stream(rx_callback, num_buffers,
            bladeRF.FORMAT_SC16_Q12, samples_per_buffer, num_transfers, self)

        self.tx_stream = self.device.tx.stream(tx_callback,  num_buffers,
            bladeRF.FORMAT_SC16_Q12, samples_per_buffer, num_transfers, self)

    def run(self):
        self.rx_stream.start()
        while self.num_filled < self.prefill_count and self.tx_idx >= 0:
            with self.samples_available:
                self.samples_available.wait()
        self.tx_stream.start()
        i = raw_input('Repeater is running, press enter to exit... ')
        with self.samples_available:
            self.rx_idx = self.tx_idx = -1
        sys.exit(0)


if __name__ == '__main__':
    config = {
        # defaults for now
        }
    r = Repeater('', config)
    r.run()
