"""\
bladeRF Repeater

Usage:
  repeater.py <rx_frequency> <tx_frequency> [options]
  repeater.py (-h | --help)
  repeater.py --version

Options:
  -h --help                Show this screen.
  -v --version             Show version.
  -d --device=<d>          Device identifier [default: ]
  -b --bandwidth=<bw>      Bandwidth in Hertz [default: 7000000].
  -s --sample-rate=<sr>    Sample rate in samples per second [default: 10000000].
  -n --num-buffers=<nb>    Number of transfer buffers [default: 32].
  -t --num-transfers=<nt>  Number of transfers [default: 1].
  -l --num-samples=<ns>    Numper of samples per transfer buffer [default: 8192].
  -g --lna-gain=<lg>       Set LNA gain [default: LNA_GAIN_MAX]
  -o --rx-vga1-gain=<lg>   Set rx vga1 [default: 21]
  -w --rx-vga2-gain=<sq>   Set rx vga2 squelch [default: 17]
  -r --tx-vga1-gain=<lg>   Set tx vga1 [default: 0]
  -u --tx-vga2-gain=<sq>   Set tx vga2 squelch [default: 0]
  -q --squelch=<sq>        Set power squelch [default: 25]
"""
import sys
import bladeRF
import threading
from numpy import vdot, log10
from docopt import docopt


class Repeater(object):

    def __init__(self, num_buffers, num_transfers, num_samples):
        self.zerobuf = bladeRF.ffi.new('int16_t[]', num_samples * 2)
        self.num_buffers = num_buffers
        self.num_filled = 0
        self.prefill_count = num_transfers + (num_buffers - num_transfers) / 2
        self.samples_available = threading.Condition()


if __name__ == '__main__':
    args = docopt(__doc__, version='bladeRF Repeater 1.0')
    device = bladeRF.Device(args['--device'])

    device.rx.enabled = True
    device.rx.frequency = int(args['<rx_frequency>'])
    device.rx.bandwidth = int(args['--bandwidth'])
    device.rx.sample_rate = int(args['--sample-rate'])
    device.rx.vga1 = int(args['--rx-vga1-gain'])
    device.rx.vga2 = int(args['--rx-vga2-gain'])

    device.lna_gain = getattr(bladeRF, args['--lna-gain'])

    device.tx.enabled = True
    device.tx.frequency = int(args['<rx_frequency>'])
    device.tx.bandwidth = int(args['--bandwidth'])
    device.tx.sample_rate = int(args['--sample-rate'])
    device.rx.vga1 = int(args['--tx-vga1-gain'])
    device.rx.vga2 = int(args['--tx-vga2-gain'])

    squelch = float(args['--squelch'])
    num_buffers = int(args['--num-buffers'])
    num_transfers = int(args['--num-transfers'])
    num_samples = int(args['--num-samples'])

    def rx(dev, stream, meta_data, samples, num_samples, repeater):
        with repeater.samples_available:
            if not stream.running:
                return
            samples = bladeRF.samples_to_narray(samples, num_samples)
            if bladeRF.squelched(samples, squelch):
                return stream.current()
            if repeater.num_filled >= 2 * repeater.num_buffers:
                # "RX Overrun encountered, stop advancing
                return stream.current()
            ret = stream.next()
            repeater.num_filled += 1
            repeater.samples_available.notify()
        return ret

    def tx(dev, stream, meta_data, samples, num_samples, repeater):
        with repeater.samples_available:
            if not stream.running:
                return
            if repeater.num_filled == 0:
                return repeater.zerobuf
            ret = stream.next()
            repeater.num_filled -= 1
        return ret

    repeater = Repeater(num_buffers, num_transfers, num_samples)

    rx_stream = device.rx.stream(
        rx,
        num_buffers,
        bladeRF.FORMAT_SC16_Q12,
        num_samples,
        num_transfers,
        repeater)

    tx_stream = device.tx.stream(
        tx,
        num_buffers,
        bladeRF.FORMAT_SC16_Q12,
        num_samples,
        num_transfers,
        repeater)

    tx_stream.buffers = rx_stream.buffers  # wire up tx buffers to rx

    rx_stream.start()
    tx_stream.start()

    i = raw_input('Repeater is running, press enter to exit... ')

    with repeater.samples_available:
        rx_stream.running = tx_stream.running = False

    rx_stream.join()
    tx_stream.join()
    sys.exit(0)
