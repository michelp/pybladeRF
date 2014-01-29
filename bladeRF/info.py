import bladeRF
from bladeRF import _cffi
from bladeRF._cffi import ffi, cdef, ptop


cdef("""
typedef enum {
    BLADERF_FPGA_UNKNOWN = 0,   /**< Unable to determine FPGA variant */
    BLADERF_FPGA_40KLE = 40,    /**< 40 kLE FPGA */
    BLADERF_FPGA_115KLE = 115   /**< 115 kLE FPGA */
} bladerf_fpga_size;
""")


@cdef('int bladerf_get_fpga_size(struct bladerf *dev, bladerf_fpga_size *size);')
def get_fpga_size(dev):
    size = ffi.new('bladerf_fpga_size *')
    err = _cffi.lib.bladerf_get_fpga_size(dev, size)
    bladeRF.errors.check_retcode(err)
    return int(size[0])




