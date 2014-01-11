from ._cffi import ffi, ptop

from .init import (
    open,
    close,
    open_device,
    get_device_list,
    free_device_list,
    )

from .ctrl import (
    enable_module,
    set_sample_rate,
    get_sampling,
    set_sampling,
    get_sample_rate,
    get_rational_sample_rate,
    set_txvga2,
    get_txvga2,
    set_txvga1,
    get_txvga1,
    set_lna_gain,
    get_lna_gain,
    set_rxvga1,
    get_rxvga1,
    set_rxvga2,
    get_rxvga2,
    set_bandwidth,
    get_bandwidth,
    set_lpf_mode,
    get_lpf_mode,
    select_band,
    set_frequency,
    get_frequency,
    )

from .data import (
    callback,
    init_stream,
    stream,
    deinit_stream,
    tx,
    rx,
    )

from .low_level import (
    get_transfer_timeout,
    set_transfer_timeout,
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

LB_BB_LPF = lib.BLADERF_LB_BB_LPF
LB_BB_VGA2 = lib.BLADERF_LB_BB_VGA2
LB_BB_OP = lib.BLADERF_LB_BB_OP
LB_RF_LNA_START = lib.BLADERF_LB_RF_LNA_START
LB_RF_LNA1 = lib.BLADERF_LB_RF_LNA1
LB_RF_LNA2 = lib.BLADERF_LB_RF_LNA2
LB_RF_LNA3 = lib.BLADERF_LB_RF_LNA3
LB_NONE = lib.BLADERF_LB_NONE

LNA_GAIN_UNKNOWN = lib.BLADERF_LNA_GAIN_UNKNOWN
LNA_GAIN_BYPASS = lib.BLADERF_LNA_GAIN_BYPASS
LNA_GAIN_MID = lib.BLADERF_LNA_GAIN_MID
LNA_GAIN_MAX = lib.BLADERF_LNA_GAIN_MAX

LPF_NORMAL = lib.BLADERF_LPF_NORMAL
LPF_BYPASSED = lib.BLADERF_LPF_BYPASSED
LPF_DISABLED = lib.BLADERF_LPF_DISABLED

FORMAT_SC16_Q12 = lib.BLADERF_FORMAT_SC16_Q12

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
    
from device import Device
