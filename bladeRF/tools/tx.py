"""\
bladeRF Transmitter

Usage:
  tx.py <frequency> [options]
  tx.py (-h | --help)
  tx.py --version

Options:
  -h --help                Show this screen.
  -v --version             Show version.
  -d --device=<d>          Device identifier [default: ]
  -f --file=<f>            File to read samples from [default: -].
  -b --bandwidth=<bw>      Bandwidth in Hertz [default: 7000000].
  -s --sample-rate=<sr>    Sample rate in samples per second [default: 10000000].
  -n --num-buffers=<nb>    Number of transfer buffers [default: 32].
  -t --num-transfers=<nt>  Number of transfers [default: 16].
  -l --num-samples=<ns>    Numper of samples per transfer buffer [default: 4096].
"""
import sys
import bladeRF
from numpy import vdot, log10
from docopt import docopt


def main():
    args = docopt(__doc__, version='bladeRF Transmitter 1.0')
    infile = sys.stdin if args['--file'] == '-' else open(args['--file'], 'rb')

    device = bladeRF.Device(args['--device'])
    device.tx.enabled = True
    device.tx.frequency = int(args['<frequency>'])
    device.tx.bandwidth = int(args['--bandwidth'])
    device.tx.sample_rate = int(args['--sample-rate'])

    def tx(device, stream, meta_data, samples, num_samples, user_data):
        next = stream.next()
        if not infile.readinto(bladeRF.ffi.buffer(next, num_samples)):
            return
        return next

    stream = device.tx.stream(
        tx,
        int(args['--num-buffers']),
        bladeRF.FORMAT_SC16_Q12,
        int(args['--num-samples']),
        int(args['--num-transfers']))

    stream.run()


if __name__ == '__main__':
    main()
