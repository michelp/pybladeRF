"""\
bladeRF Receiver

Usage:
  rx.py <frequency> [options]
  rx.py (-h | --help)
  rx.py --version

Options:
  -h --help                Show this screen.
  -v --version             Show version.
  -d --device=<d>          Device identifier [default: ]
  -f --file=<f>            File to write samples to [default: -].
  -b --bandwidth=<bw>      Bandwidth in Hertz [default: 7000000].
  -s --sample-rate=<sr>    Sample rate in samples per second [default: 10000000].
  -n --num-buffers=<nb>    Number of transfer buffers [default: 16].
  -t --num-transfers=<nt>  Number of transfers [default: 16].
  -l --num-samples=<ns>    Numper of samples per transfer buffer [default: 8192].
  -g --lna-gain=<g>        Set LNA gain [default: LNA_GAIN_MAX]
  -o --rx-vga1=<g>         Set vga1 [default: 21]
  -w --rx-vga2=<g>         Set vga2 squelch [default: 18]
  -q --squelch=<sq>        Set squelch [default: 0]
  -e --decimate=<f>        Decimate factor [default: 0]
"""
import sys
import bladeRF
from docopt import docopt


def get_args():
    return docopt(__doc__, version='bladeRF Receiver 1.0')


def get_stream(args):
    outfile = sys.stdout if args['--file'] == '-' else open(args['--file'], 'wb')
    device = bladeRF.Device(args['--device'])
    device.rx.enabled = True
    device.rx.frequency = int(args['<frequency>'])
    device.rx.bandwidth = int(args['--bandwidth'])
    device.rx.sample_rate = int(args['--sample-rate'])
    device.lna_gain = getattr(bladeRF, args['--lna-gain'])
    device.rx.vga1 = int(args['--rx-vga1'])
    device.rx.vga2 = int(args['--rx-vga2'])
    squelch = float(args['--squelch'])

    def rx(device, stream, meta_data, samples, num_samples, user_data):
        if squelch:
            samples = bladeRF.samples_to_narray(samples, num_samples)
            if bladeRF.squelched(samples, squelch):
                return stream.current()

        buff = stream.current_as_buffer()
        outfile.write(buff)
        return stream.next()


    stream = device.rx.stream(
        rx,
        int(args['--num-buffers']),
        bladeRF.FORMAT_SC16_Q11,
        int(args['--num-samples']),
        int(args['--num-transfers']),
        )
    return stream


def main():
    get_stream(get_args()).run()


if __name__ == '__main__':
    main()
