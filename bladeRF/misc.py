import bladeRF
from bladeRF import _cffi
from bladeRF._cffi import ffi, cdef, ptop


cdef("""
typedef enum {
    BLADERF_LOG_LEVEL_VERBOSE,  /**< Verbose level logging */
    BLADERF_LOG_LEVEL_DEBUG,    /**< Debug level logging */
    BLADERF_LOG_LEVEL_INFO,     /**< Information level logging */
    BLADERF_LOG_LEVEL_WARNING,  /**< Warning level logging */
    BLADERF_LOG_LEVEL_ERROR,    /**< Error level logging */
    BLADERF_LOG_LEVEL_CRITICAL, /**< Fatal error level logging */
    BLADERF_LOG_LEVEL_SILENT    /**< No output */
} bladerf_log_level;
""")


@cdef('void bladerf_log_set_verbosity(bladerf_log_level level);')
def log_set_verbosity(level):
    _cffi.lib.bladerf_log_set_verbosity(level)
    
