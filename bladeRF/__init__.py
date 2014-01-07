from ._cffi import ffi, ptop

from .init import (
    open,
    get_device_list,
    free_device_list,
    )

from .ctrl import (
    enable_module,
    set_sample_rate,
    get_sampling,
    set_sampling,
    get_sample_rate,
    )

import bladeRF._cffi

# compilation happens here in verify(),
# all C code must be defined at this point
# and only after here may the library functions
# and constants be accessed. hence the many import
# name tricks used through the implementation

# http://explosm.net/comics/420/

bladeRF._cffi.lib = lib = ffi.verify("""
#include <libbladeRF.h>
""", libraries=['bladeRF'])

MODULE_TX = lib.BLADERF_MODULE_TX
MODULE_RX = lib.BLADERF_MODULE_RX

SAMPLING_UNKNOWN = lib.BLADERF_SAMPLING_UNKNOWN
SAMPLING_INTERNAL = lib.BLADERF_SAMPLING_INTERNAL
SAMPLING_EXTERNAL = lib.BLADERF_SAMPLING_EXTERNAL

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
    
