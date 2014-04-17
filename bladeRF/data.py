import bladeRF
from bladeRF import _cffi
from bladeRF._cffi import ffi, cdef, ptop

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
    uint64_t timestamp;     /**< Timestamp (TODO format TBD) */
    uint32_t flags;         /**< Metadata format flags */
    uint32_t status;         /**< Metadata format status */
};

""")

def raw_callback(f):
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


@cdef("""int bladerf_sync_config(struct bladerf *dev,
                                 bladerf_module module,
                                 bladerf_format format,
                                 unsigned int num_buffers,
                                 unsigned int buffer_size,
                                 unsigned int num_transfers,
                                 unsigned int stream_timeout);""")
def sync_config(dev, module, format, num_buffers, buffer_size, num_transfers, stream_timeout):
    err = _cffi.lib.bladerf_sync_config(dev, module, format, num_buffers, buffer_size, num_transfers, stream_timeout)
    bladeRF.errors.check_retcode(err)


@cdef("""int bladerf_sync_tx(struct bladerf *dev,
                            void *samples, unsigned int num_samples,
                            struct bladerf_metadata *metadata,
                            unsigned int timeout_ms);""")
def tx(dev, samples, num_samples, metadata, timeout_ms):
    err = _cffi.lib.bladerf_sync_tx(dev, samples, num_samples, metadata, timeout_ms)
    bladeRF.errors.check_retcode(err)


@cdef("""int bladerf_sync_rx(struct bladerf *dev,
                             void *samples, unsigned int num_samples,
                             struct bladerf_metadata *metadata,
                             unsigned int timeout_ms);""")
def rx(dev, samples, num_samples, metadata, timeout_ms):
    err = _cffi.lib.bladerf_sync_rx(dev, samples, num_samples, metadata, timeout_ms)
    bladeRF.errors.check_retcode(err)

