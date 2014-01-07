from contextlib import contextmanager

import bladeRF
from bladeRF import _cffi
from bladeRF._cffi import ffi, cdef, ptop


@cdef('void bladerf_free_device_list(struct bladerf_devinfo *devices);')
def free_device_list(devices):
    _cffi.lib.bladerf_free_device_list(devices[0])


@cdef('int bladerf_get_device_list(struct bladerf_devinfo **devices);')
def get_device_list():
    devices = ffi.gc(
        ptop('struct bladerf_devinfo'),
        free_device_list)
    size = _cffi.lib.bladerf_get_device_list(devices)
    bladeRF.errors.check_retcode(size)
    return (size, devices)


cdef('int bladerf_open('
     'struct bladerf **device, '
     'const char *device_identifier);')
cdef('void bladerf_close(struct bladerf *device);')

@contextmanager
def open(device_identifier=''):
        device = ptop('struct bladerf')
        err = _cffi.lib.bladerf_open(device, device_identifier)
        bladeRF.errors.check_retcode(err)
        yield device[0]
        _cffi.lib.bladerf_close(device[0])


