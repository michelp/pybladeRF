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


@cdef('int bladerf_open(struct bladerf **device, '
      'const char *device_identifier);')
def open(device_identifier=''):
    device = ptop('struct bladerf')
    err = _cffi.lib.bladerf_open(device, device_identifier)
    bladeRF.errors.check_retcode(err)
    return device


@cdef('void bladerf_close(struct bladerf *device);')
def close(device):
    _cffi.lib.bladerf_close(device)


@contextmanager
def open_device(device_identifier=''):
    device = open(device_identifier)
    yield device[0]
    close(device[0])
