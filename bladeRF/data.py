import bladeRF
from bladeRF import _cffi
from bladeRF._cffi import ffi, cdef, ptop

has_numpy = True
try:
    import numpy as np
except ImportError:
    has_numpy = False


cdef("""
typedef enum {
    BLADERF_FORMAT_SC16_Q12, /**< Signed, Complex 16-bit Q12.
                               *  This is the native format of the DAC data.
                               *
                               *  Samples are interleaved IQ value pairs, where
                               *  each value in the pair is an int16_t. For each
                               *  value, the data in the lower bits. The upper
                               *  bits are reserved.
                               *
                               *  When using this format, note that buffers
                               *  must be at least
                               *       2 * num_samples * sizeof(int16_t)
                               *  bytes large
                               */
} bladerf_format;

/**
 * For both RX and TX, the stream callback receives:
 * dev:             Device structure
 * stream:          The associated stream
 * metadata:        TBD
 * user_data:       User data provided when initializing stream
 *
 * <br>
 *
 * For TX callbacks:
 *  samples:        Pointer fo buffer of samples that was sent
 *  num_samples:    Number of sent in last transfer and to send in next transfer
 *
 *  Return value:   The user specifies the address of the next buffer to send
 *
 * For RX callbacks:
 *  samples:        Buffer filled with received data
 *  num_samples:    Number of samples received and size of next buffers
 *
 *  Return value:   The user specifies the next buffer to fill with RX data,
 *                  which should be num_samples in size.
 *
 */

typedef void *(*bladerf_stream_cb)(struct bladerf *dev,
                                   struct bladerf_stream *stream,
                                   struct bladerf_metadata *meta,
                                   void *samples,
                                   size_t num_samples,
                                   void *user_data);


struct bladerf_metadata {
    uint32_t version;       /**< Metadata format version */
    uint64_t timestamp;     /**< Timestamp (TODO format TBD) */
};

""")

def callback(f):
    @ffi.callback('bladerf_stream_cb')
    def handler(dev, stream, meta, samples, num_samples, user_data):
        user_data = ffi.from_handle(user_data)
        v = f(dev, stream, meta, samples, num_samples, user_data)
        if v is None:
            return ffi.NULL
        return v
    return handler


@cdef("""
int  bladerf_init_stream(struct bladerf_stream **stream,
                         struct bladerf *dev,
                         bladerf_stream_cb callback,
                         void ***buffers,
                         size_t num_buffers,
                         bladerf_format format,
                         size_t num_samples,
                         size_t num_transfers,
                         void *user_data);
""")
def init_stream(dev, callback, num_buffers, format, num_samples, num_transfers,
                user_data):
    stream = ffi.new('struct bladerf_stream*[1]')
    buffers = ffi.new('void**[1]')
    err = _cffi.lib.bladerf_init_stream(
        stream, dev, callback, buffers, num_buffers, format, num_samples,
        num_transfers, user_data)
    bladeRF.errors.check_retcode(err)
    return (stream[0], buffers[0])


@cdef('int bladerf_stream(struct bladerf_stream *stream, bladerf_module module);')
def stream(stream, module):
    err = _cffi.lib.bladerf_stream(stream, module)
    bladeRF.errors.check_retcode(err)


@cdef('void bladerf_deinit_stream(struct bladerf_stream *stream);')
def deinit_stream(stream):
    _cffi.lib.bladerf_deinit_stream(stream)


@cdef('int bladerf_tx(struct bladerf *dev, bladerf_format format,'
      'void *samples, int num_samples, struct bladerf_metadata *metadata);')
def tx(dev, format, samples, num_samples, metadata=None):
    if metadata is None:
        metadata = ffi.new('struct bladerf_metadata*')  #  currently unused
    err = _cffi.lib.bladerf_tx(dev, format, str(samples), num_samples, metadata)
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_rx(struct bladerf *dev, bladerf_format format,'
      'void *samples, int num_samples, struct bladerf_metadata *metadata);')
def rx(dev, format, num_samples, metadata=None):
    if metadata is None:
        metadata = ffi.new('struct bladerf_metadata*')
    samples = ffi.new('int16_t[]', 2 * num_samples)
    err = _cffi.lib.bladerf_rx(dev, format, samples, num_samples, metadata)
    bladeRF.errors.check_retcode(err)
    return bytearray(ffi.buffer(samples))


def rx_np(dev, format, num_samples, metadata=None):
    data = rx(dev, format, num_samples, metadata)

    if has_numpy:
        # use NumPy array
        iq = np.empty(len(bytes)//2, 'complex')
        iq.real, iq.imag = bytes[::2], bytes[1::2]
        iq /= (255/2)
        iq -= (1 + 1j)
        return iq
    raise NotImplementedError('install numpy.')
