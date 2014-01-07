from bladeRF import _cffi

class BladeRFException(Exception): pass
class UnexpectedError(BladeRFException): pass
class RangeError(BladeRFException): pass
class InvalError(BladeRFException): pass
class MemError(BladeRFException): pass
class BladeIOError(BladeRFException): pass  # IOError conflicts with builtin
class TimeoutError(BladeRFException): pass
class NodevError(BladeRFException): pass
class UnsupportedError(BladeRFException): pass
class MisalignedError(BladeRFException): pass
class ChecksumError(BladeRFException): pass

errors = {
    _cffi.lib.BLADERF_ERR_UNEXPECTED: UnexpectedError,
    _cffi.lib.BLADERF_ERR_RANGE: RangeError,
    _cffi.lib.BLADERF_ERR_INVAL: InvalError,
    _cffi.lib.BLADERF_ERR_MEM: MemError,
    _cffi.lib.BLADERF_ERR_IO: BladeIOError,
    _cffi.lib.BLADERF_ERR_TIMEOUT: TimeoutError,
    _cffi.lib.BLADERF_ERR_NODEV: NodevError,
    _cffi.lib.BLADERF_ERR_UNSUPPORTED: UnsupportedError,
    _cffi.lib.BLADERF_ERR_MISALIGNED: MisalignedError,
    _cffi.lib.BLADERF_ERR_CHECKSUM: ChecksumError,
}

def check_retcode(code, *args, **kwargs):
    if code < 0:
        if code not in errors:
            raise TypeError('No such retcode %s' % code)
        raise errors[code](*args, **kwargs)
