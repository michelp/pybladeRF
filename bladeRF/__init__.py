from ._cffi import ffi, ptop

has_numpy = True
try:
    import numpy as np
except ImportError:
    has_numpy = False

from .init import (
    open,
    close,
    open_device,
    get_device_list,
    free_device_list,
    )

from .ctrl import (
    enable_module,
    set_sample_rate,
    get_sampling,
    set_sampling,
    get_sample_rate,
    get_rational_sample_rate,
    set_txvga2,
    get_txvga2,
    set_txvga1,
    get_txvga1,
    set_lna_gain,
    get_lna_gain,
    set_rxvga1,
    get_rxvga1,
    set_rxvga2,
    get_rxvga2,
    set_bandwidth,
    get_bandwidth,
    set_lpf_mode,
    get_lpf_mode,
    select_band,
    set_frequency,
    get_frequency,
    )

from .data import (
    raw_callback,
    init_stream,
    stream,
    deinit_stream,
    tx,
    rx,
    sync_config,
    )

from .misc import (
    log_set_verbosity,
    )

from .info import (
    get_fpga_size,
    )

import bladeRF._cffi

# compilation happens here in verify(),
# all C code must be defined at this point
# and only after here may the library functions
# and constants be accessed. hence the many import
# name tricks used through the implementation

# http://explosm.net/comics/420/

ffi.cdef("""
float* samples_to_floats(void*, int);

void free(void *ptr);
""")

bladeRF._cffi.lib = lib = ffi.verify("""
#include <libbladeRF.h>
#include <stdlib.h>

/* this helper function is to turn the two 16 bit ints per sample into
 two normalized floats, so that it can be passed directly to
 numpy.frombuffer which can only take two 32-bit floats and turn them
 into a complex64 */

float* samples_to_floats(void *samples, int num_samples) {
    int i;
    int16_t* data = (int16_t*)samples;
    float* buffer = (float*)malloc(2 * num_samples * sizeof(float));
    for (i = 0; i < num_samples; i++) {
        buffer[i] = (float)data[i] * (1.0f/2048.0f);
    }
    return buffer;
}

""", libraries=['bladeRF'])


def samples_to_floats(samples, num_samples):
    """Call optimized C function to alocate and return pointer to
    buffer full of normalized I/Q floats.
    """
    return ffi.gc(lib.samples_to_floats(samples, num_samples), lib.free)


def to_float_buffer(raw_samples, num_samples):
    """Return an FFI buffer of I/Q floats."""
    return bladeRF.ffi.buffer(samples_to_floats(raw_samples, num_samples), 2*num_samples*bladeRF.ffi.sizeof('float'))


if has_numpy:
    def samples_to_narray(samples, num_samples):
        """Return a numpy array of type complex64 from the samples."""
        return np.frombuffer(to_float_buffer(samples, num_samples), np.complex64)


MODULE_TX = lib.BLADERF_MODULE_TX
MODULE_RX = lib.BLADERF_MODULE_RX

SAMPLING_UNKNOWN = lib.BLADERF_SAMPLING_UNKNOWN
SAMPLING_INTERNAL = lib.BLADERF_SAMPLING_INTERNAL
SAMPLING_EXTERNAL = lib.BLADERF_SAMPLING_EXTERNAL

LNA_GAIN_UNKNOWN = lib.BLADERF_LNA_GAIN_UNKNOWN
LNA_GAIN_BYPASS = lib.BLADERF_LNA_GAIN_BYPASS
LNA_GAIN_MID = lib.BLADERF_LNA_GAIN_MID
LNA_GAIN_MAX = lib.BLADERF_LNA_GAIN_MAX

RXVGA1_GAIN_MIN = lib.BLADERF_RXVGA1_GAIN_MIN
RXVGA1_GAIN_MAX = lib.BLADERF_RXVGA1_GAIN_MAX
RXVGA2_GAIN_MIN = lib.BLADERF_RXVGA2_GAIN_MIN
RXVGA2_GAIN_MAX = lib.BLADERF_RXVGA2_GAIN_MAX
TXVGA1_GAIN_MIN = lib.BLADERF_TXVGA1_GAIN_MIN
TXVGA1_GAIN_MAX = lib.BLADERF_TXVGA1_GAIN_MAX
TXVGA2_GAIN_MIN = lib.BLADERF_TXVGA2_GAIN_MIN
TXVGA2_GAIN_MAX = lib.BLADERF_TXVGA2_GAIN_MAX
SAMPLERATE_MIN = lib.BLADERF_SAMPLERATE_MIN
SAMPLERATE_REC_MAX = lib.BLADERF_SAMPLERATE_REC_MAX
BANDWIDTH_MIN = lib.BLADERF_BANDWIDTH_MIN
BANDWIDTH_MAX = lib.BLADERF_BANDWIDTH_MAX
FREQUENCY_MIN = lib.BLADERF_FREQUENCY_MIN
FREQUENCY_MAX = lib.BLADERF_FREQUENCY_MAX

LPF_NORMAL = lib.BLADERF_LPF_NORMAL
LPF_BYPASSED = lib.BLADERF_LPF_BYPASSED
LPF_DISABLED = lib.BLADERF_LPF_DISABLED

FORMAT_SC16_Q11 = lib.BLADERF_FORMAT_SC16_Q11

LOG_LEVEL_VERBOSE = lib.BLADERF_LOG_LEVEL_VERBOSE
LOG_LEVEL_DEBUG = lib.BLADERF_LOG_LEVEL_DEBUG
LOG_LEVEL_INFO = lib.BLADERF_LOG_LEVEL_INFO
LOG_LEVEL_WARNING = lib.BLADERF_LOG_LEVEL_WARNING
LOG_LEVEL_ERROR = lib.BLADERF_LOG_LEVEL_ERROR
LOG_LEVEL_CRITICAL = lib.BLADERF_LOG_LEVEL_CRITICAL
LOG_LEVEL_SILENT = lib.BLADERF_LOG_LEVEL_SILENT


from .errors import (
    BladeRFException,
    UnexpectedError,
    RangeError,
    InvalError,
    MemError,
    BladeIOError,
    TimeoutError,
    NodevError,
    UnsupportedError,
    MisalignedError,
    ChecksumError,
    )

from device import (
    Device,
    )


def power(samples):
    return 10*np.log10(np.abs(np.vdot(samples, samples)))


def squelched(samples, level):
    return power(samples) < level
