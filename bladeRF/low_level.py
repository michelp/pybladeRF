import bladeRF
from bladeRF import _cffi
from bladeRF._cffi import ffi, cdef, ptop


@cdef('void bladerf_set_transfer_timeout(struct bladerf *dev,'
      'bladerf_module module, int timeout);')
def set_transfer_timeout(dev, module, timeout):
    _cffi.lib.bladerf_set_transfer_timeout(dev, module, timeout)

@cdef('int bladerf_get_transfer_timeout(struct bladerf *dev, bladerf_module module,'
      'unsigned int *timeout);')
def get_transfer_timeout(dev, module):
    timeout = ffi.new('unsigned int*')
    err = _cffi.lib.bladerf_get_transfer_timeout(dev, module, timeout)
    bladeRF.errors.check_retcode(err)
    return timeout[0]
    


