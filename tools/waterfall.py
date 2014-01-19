import sys
import bladeRF
import threading


@bladeRF.callback
def rx_callback(device, stream, meta_data,
                samples, num_samples, user_data):
    self = user_data
    with self.samples_available:
        if self.rx_idx < 0:
            return
        self.rx_idx += 1
        ret = self.rx_stream.buffers[self.rx_idx]
        if self.rx_idx >= self.num_buffers:
            self.rx_idx = 0;

        if self.num_filled >= 2 * self.num_buffers:
            print "RX Overrun encountered. Terminating RX task."
            return

        self.num_filled += 1
        self.samples_available.notify()
    return ret


class Waterfall(object):

    def __init__(self, device_indentifier, config,
                 num_transfers=16,
                 samples_per_buffer=8192,
                 num_buffers=32):

        self.device = bladeRF.Device.from_params(device_indentifier, **config)

        self.rx_stream = self.device.rx.stream(
            rx_callback, num_buffers,
            bladeRF.FORMAT_SC16_Q12,
            samples_per_buffer, num_transfers, self)

    def run(self):
        self.rx_stream.start()
        i = raw_input('Running, press any key to exit... ')
        sys.exit(0)


if __name__ == '__main__':
    config = {
        # defaults for now
        }
    r = Repeater('', config)
    r.run()
