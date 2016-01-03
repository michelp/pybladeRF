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

typedef enum {
    BLADERF_LNA_GAIN_UNKNOWN,    /**< Invalid LNA gain */
    BLADERF_LNA_GAIN_BYPASS,     /**< LNA bypassed - 0dB gain */
    BLADERF_LNA_GAIN_MID,        /**< LNA Mid Gain (MAX-6dB) */
    BLADERF_LNA_GAIN_MAX         /**< LNA Max Gain */
} bladerf_lna_gain;

typedef enum {
    BLADERF_LPF_NORMAL,     /**< LPF connected and enabled */
    BLADERF_LPF_BYPASSED,   /**< LPF bypassed */
    BLADERF_LPF_DISABLED    /**< LPF disabled */
} bladerf_lpf_mode;


/** Minimum RXVGA1 gain, in dB */
#define BLADERF_RXVGA1_GAIN_MIN ...

/** Maximum RXVGA1 gain, in dB */
#define BLADERF_RXVGA1_GAIN_MAX ...

/** Minimum RXVGA2 gain, in dB */
#define BLADERF_RXVGA2_GAIN_MIN ...

/** Maximum RXVGA2 gain, in dB */
#define BLADERF_RXVGA2_GAIN_MAX ...

/** Minimum TXVGA1 gain, in dB */
#define BLADERF_TXVGA1_GAIN_MIN ...

/** Maximum TXVGA1 gain, in dB */
#define BLADERF_TXVGA1_GAIN_MAX ...

/** Minimum TXVGA2 gain, in dB */
#define BLADERF_TXVGA2_GAIN_MIN ...

/** Maximum TXVGA2 gain, in dB */
#define BLADERF_TXVGA2_GAIN_MAX ...

/** Minimum sample rate, in Hz */
#define BLADERF_SAMPLERATE_MIN ...

/** Maximum recommended sample rate, in Hz */
#define BLADERF_SAMPLERATE_REC_MAX ...

/** Minimum bandwidth, in Hz */
#define BLADERF_BANDWIDTH_MIN ...

/** Maximum bandwidth, in Hz */
#define BLADERF_BANDWIDTH_MAX ...

/** Minimum tunable frequency (without an XB-200 attached), in Hz */
#define BLADERF_FREQUENCY_MIN ...

/** Maximum tunable frequency, in Hz */
#define BLADERF_FREQUENCY_MAX ...
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
    err = _cffi.lib.bladerf_set_sample_rate(dev, module, int(rate), actual)
    bladeRF.errors.check_retcode(err)
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
    err = _cffi.lib.bladerf_get_sample_rate(dev, module, rate)
    bladeRF.errors.check_retcode(err)
    return int(rate[0])


@cdef('int bladerf_get_rational_sample_rate(struct bladerf *dev,'
      'bladerf_module module, struct bladerf_rational_rate *rate);')
def get_rational_sample_rate(dev, module):
    pass


@cdef('int bladerf_set_txvga2(struct bladerf *dev, int gain);')
def set_txvga2(dev, gain):
    err = _cffi.lib.bladerf_set_txvga2(dev, gain)
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_get_txvga2(struct bladerf *dev, int *gain);')
def get_txvga2(dev):
    gain = ffi.new('int *')
    err = _cffi.lib.bladerf_get_txvga2(dev, gain)
    bladeRF.errors.check_retcode(err)
    return int(gain[0])


@cdef('int bladerf_set_txvga1(struct bladerf *dev, int gain);')
def set_txvga1(dev, gain):
    err = _cffi.lib.bladerf_set_txvga1(dev, gain)
    bladeRF.errors.check_retcode(err)
    

@cdef('int bladerf_get_txvga1(struct bladerf *dev, int *gain);')
def get_txvga1(dev):
    gain = ffi.new('int *')
    err = _cffi.lib.bladerf_get_txvga1(dev, gain)
    bladeRF.errors.check_retcode(err)
    return int(gain[0])


@cdef('int bladerf_set_lna_gain(struct bladerf *dev, bladerf_lna_gain gain);')
def set_lna_gain(dev, gain):
    err = _cffi.lib.bladerf_set_lna_gain(dev, gain)
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_get_lna_gain(struct bladerf *dev, bladerf_lna_gain *gain);')
def get_lna_gain(dev):
    gain = ffi.new('bladerf_lna_gain *')
    err = _cffi.lib.bladerf_get_lna_gain(dev, gain)
    bladeRF.errors.check_retcode(err)
    return int(gain[0])


@cdef('int bladerf_set_rxvga1(struct bladerf *dev, int gain);')
def set_rxvga1(dev, gain):
    err = _cffi.lib.bladerf_set_rxvga1(dev, gain)
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_get_rxvga1(struct bladerf *dev, int *gain);')
def get_rxvga1(dev):
    gain = ffi.new('int *')
    err = _cffi.lib.bladerf_get_rxvga1(dev, gain)
    bladeRF.errors.check_retcode(err)
    return int(gain[0])


@cdef('int bladerf_set_rxvga2(struct bladerf *dev, int gain);')
def set_rxvga2(dev, gain):
    err = _cffi.lib.bladerf_set_rxvga2(dev, gain)
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_get_rxvga2(struct bladerf *dev, int *gain);')
def get_rxvga2(dev):
    gain = ffi.new('int *')
    err = _cffi.lib.bladerf_get_rxvga2(dev, gain)
    bladeRF.errors.check_retcode(err)
    return int(gain[0])


@cdef('int bladerf_set_bandwidth(struct bladerf *dev, bladerf_module module, '
      'unsigned int bandwidth, unsigned int *actual);')
def set_bandwidth(dev, module, bandwidth):
    actual = ffi.new('unsigned int *')
    err = _cffi.lib.bladerf_set_bandwidth(dev, module, bandwidth, actual)
    bladeRF.errors.check_retcode(err)
    return int(actual[0])


@cdef('int bladerf_get_bandwidth(struct bladerf *dev, bladerf_module module, '
      'unsigned int *bandwidth);')
def get_bandwidth(dev, module):
    bandwidth = ffi.new('unsigned int *')
    err = _cffi.lib.bladerf_get_bandwidth(dev, module, bandwidth)
    bladeRF.errors.check_retcode(err)
    return int(bandwidth[0])


@cdef('int bladerf_set_lpf_mode(struct bladerf *dev, bladerf_module module, '
      'bladerf_lpf_mode mode);')
def set_lpf_mode(dev, module, mode):
    err = _cffi.lib.bladerf_set_lpf_mode(dev, module, mode)
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_get_lpf_mode(struct bladerf *dev, bladerf_module module,'
      'bladerf_lpf_mode *mode);')
def get_lpf_mode(dev, module):
    mode = ffi.new('bladerf_lpf_mode *')
    err = _cffi.lib.bladerf_get_lpf_mode(dev, module, mode)
    bladeRF.errors.check_retcode(err)
    return int(mode[0])


@cdef('int bladerf_select_band(struct bladerf *dev, bladerf_module module,'
      'unsigned int frequency);')
def select_band(dev, module, frequency):
    err = _cffi.lib.bladerf_select_band(dev, module, frequency)
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_set_frequency(struct bladerf *dev, '
      'bladerf_module module, unsigned int frequency);')
def set_frequency(dev, module, frequency):
    err = _cffi.lib.bladerf_set_frequency(dev, module, int(frequency))
    bladeRF.errors.check_retcode(err)


@cdef('int bladerf_get_frequency(struct bladerf *dev,'
      'bladerf_module module, unsigned int *frequency);')
def get_frequency(dev, module):
    frequency = ffi.new('unsigned int *')
    err = _cffi.lib.bladerf_get_frequency(dev, module, frequency)
    bladeRF.errors.check_retcode(err)
    return int(frequency[0])

