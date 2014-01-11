import bladeRF
from bladeRF import _cffi
from bladeRF._cffi import ffi, cdef, ptop


@cdef('void bladerf_set_transfer_timeout(struct bladerf *dev,'
      'bladerf_module module, int timeout);')
def set_transfer_timeout(dev, module, timeout):
    _cffi.lib.bladerf_set_transfer_timeout(dev, module, timeout)

@cdef('int get_transfer_timeout(struct bladerf *dev, bladerf_module module);')
def get_transfer_timeout(dev, module):
    return _cffi.lib.get_transfer_timeout(dev, module)

