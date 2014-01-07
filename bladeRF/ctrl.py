import bladeRF
from bladeRF import _cffi
from bladeRF._cffi import ffi, cdef, ptop

cdef("""
typedef enum
{
    BLADERF_MODULE_RX,  /**< Receive Module */
    BLADERF_MODULE_TX   /**< Transmit Module */
} bladerf_module;

typedef enum {
    BLADERF_SAMPLING_UNKNOWN,  /**< Unable to determine connection type */
    BLADERF_SAMPLING_INTERNAL, /**< Sample from RX/TX connector */
    BLADERF_SAMPLING_EXTERNAL  /**< Sample from J60 or J61 */
} bladerf_sampling;
""")

@cdef('int bladerf_enable_module(struct bladerf *dev, '
      'bladerf_module m, bool enable);')
def enable_module(dev, module, enable):
    err = _cffi.lib.bladerf_enable_module(dev, module, enable)
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_set_sample_rate(struct bladerf *dev, '
      'bladerf_module module, unsigned int rate, unsigned int *actual);')
def set_sample_rate(dev, module, rate):
    actual = ffi.new('unsigned int*')
    err = _cffi.lib.bladerf_set_sample_rate(dev, module, rate, actual)
    return int(actual[0])


@cdef('int bladerf_set_sampling(struct bladerf *dev, bladerf_sampling sampling);')
def set_sampling(dev, sampling):
    err = _cffi.lib.bladerf_set_sampling(dev, sampling)
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_get_sampling(struct bladerf *dev, bladerf_sampling *sampling);')
def get_sampling(dev):
    sampling = ffi.new('bladerf_sampling*')
    err = _cffi.lib.bladerf_get_sampling(dev, sampling)
    bladeRF.errors.check_retcode(err)
    return int(sampling[0])


@cdef('int bladerf_get_sample_rate(struct bladerf *dev, bladerf_module module, unsigned int *rate);')
def get_sample_rate(dev, module):
    rate = ffi.new('unsigned int *')
    err = _cffi.lib.bladerf_get_sample_rate(dev, module)
    bladeRF.errors.check_retcode(err)
    return int(rate[0])

