"""\
bladeRF Receiver

Usage:
  rx.py <frequency> [--device=<d> | --file=<f> | --bandwidth=<bw> | --sample-rate=<sr> | --num-buffers=<nb> | --num-transfers=<nt> | --num-samples=<ns>]
  rx.py (-h | --help)
  rx.py --version

Options:
  -h --help           Show this screen.
  --version           Show version.
  --device=<d>        Device identifier [default: ]
  --file=<f>          File to write samples to [default: -].
  --bandwidth=<bw>    Bandwidth in Hertz [default: 7000000].
  --sample-rate=<sr>  Sample rate in samples per second [default: 10000000].
  --num-buffers=<nb>    Number of transfer buffers [default: 32].
  --num-transfers=<nt>    Number of transfers [default: 16].
  --num-samples=<ns>  Numper of samples per transfer buffer [default: 8192].
"""

import sys
import bladeRF
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='bladeRF Receiver 1.0')
    outfile = sys.stdout if arguments['--file'] == '-' else open(arguments['--file'], 'wb')

    def rx(device, stream, meta_data, samples, num_samples, user_data):
        outfile.write(bladeRF.ffi.buffer(samples, num_samples*4))
        return stream.next()

    device = bladeRF.Device.from_params(
        arguments['--device'],
        rx_frequency=int(arguments['<frequency>']),
        rx_bandwidth=int(arguments['--bandwidth']),
        rx_sample_rate=int(arguments['--sample-rate']))

    stream = device.rx.stream(rx, int(arguments['--num-buffers']), bladeRF.FORMAT_SC16_Q12,
                              int(arguments['--num-samples']), int(arguments['--num-transfers']))
    stream.run()



