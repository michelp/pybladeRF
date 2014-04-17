from threading import Thread, RLock
import weakref
import bladeRF


sample_size = bladeRF.ffi.sizeof('int16_t') * 2


class Stream(Thread):
    """
    A bladeRF stream of data and a thread to process streams

This condition from the documents still holds:

 * When running a full-duplex configuration with two threads (e.g,
 * one thread calling bladerf_stream() for TX, and another for RX), stream
 * callbacks may be executed in either thread. Therefore, the caller is
 * responsible for ensuring that his or her callbacks are thread-safe. For the
 * same reason, it is highly recommended that callbacks do not block.
    """

    def __init__(self, device, module, callback,
                 num_buffers, format, num_samples,
                 num_transfers, user_data=None):
        Thread.__init__(self)
        self.running = True
        self.current_buff = 0
        self.num_buffers = num_buffers
        self.device = device
        self.module = module

        @bladeRF.ffi.callback('bladerf_stream_cb')
        def raw_callback(raw_device, raw_stream, meta, raw_samples, num_samples, user_data):
            user_data = bladeRF.ffi.from_handle(user_data)
            v = callback(self.device, self, meta, raw_samples, num_samples, user_data)
            if v is None:
                return bladeRF.ffi.NULL
            return v

        self.num_samples = num_samples
        self.callback = callback
        self.raw_callback = raw_callback
        self.user_data_handle = bladeRF.ffi.new_handle(user_data)
        self.raw_stream, self.buffers = bladeRF.init_stream(
            self.device.raw_device, raw_callback, num_buffers, format,
            num_samples, num_transfers, self.user_data_handle)

    def next(self):
        if not self.running:
            return
        ret = self.current()
        self.current_buff += 1
        if self.current_buff >= self.num_buffers:
            self.current_buff = 0
        return ret

    def current(self):
        return self.buffers[self.current_buff]

    def current_as_buffer(self):
        return bladeRF.ffi.buffer(self.current(), self.num_samples*sample_size)

    def run(self):
        bladeRF.stream(self.raw_stream, self.module)


class Module(object):
    """ A module, either rx or tx.
    """

    def __init__(self, device, module):
        self.device = device
        self.raw_device = device.raw_device
        self.module = module

    @property
    def enabled(self):
        return bladeRF.enable_module(self.raw_device, self.module, True)

    @enabled.setter
    def enabled(self, enabled):
        bladeRF.enable_module(self.raw_device, self.module, enabled)

    @property
    def frequency(self):
        return bladeRF.get_frequency(self.raw_device, self.module)

    @frequency.setter
    def frequency(self, frequency):
        bladeRF.set_frequency(self.raw_device, self.module, frequency)

    @property
    def bandwidth(self):
        return bladeRF.get_bandwidth(self.raw_device, self.module)

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        bladeRF.set_bandwidth(self.raw_device, self.module, bandwidth)

    @property
    def sample_rate(self):
        return bladeRF.get_sample_rate(self.raw_device, self.module)

    @sample_rate.setter
    def sample_rate(self, sample_rate):
        bladeRF.set_sample_rate(self.raw_device, self.module, sample_rate)

    @property
    def vga1(self):
        if self.module == bladeRF.MODULE_RX:
            return bladeRF.get_rxvga1(self.raw_device)
        else:
            return bladeRF.get_txvga1(self.raw_device)

    @vga1.setter
    def vga1(self, gain):
        if self.module == bladeRF.MODULE_RX:
            return bladeRF.set_rxvga1(self.raw_device, gain)
        else:
            return bladeRF.set_txvga1(self.raw_device, gain)

    @property
    def vga2(self):
        if self.module == bladeRF.MODULE_RX:
            return bladeRF.get_rxvga2(self.raw_device)
        else:
            return bladeRF.get_txvga2(self.raw_device)

    @vga2.setter
    def vga2(self, gain):
        if self.module == bladeRF.MODULE_RX:
            return bladeRF.set_rxvga2(self.raw_device, gain)
        else:
            return bladeRF.set_txvga2(self.raw_device, gain)

    def stream(self, callback, num_buffers, format, num_samples,
               num_transfers, user_data=None):
        return Stream(self, self.module, callback,
                      num_buffers, format, num_samples,
                      num_transfers, user_data=user_data)

    def config(self, format, num_buffers, buffer_size, num_transfers, stream_timeout=0):
        return bladeRF.sync_config(self.raw_device, self.module, format, num_buffers,
                                   buffer_size, num_transfers, stream_timeout)

    def __call__(self, num_samples, samples=None, metadata=bladeRF.ffi.NULL, timeout_ms=0):
        if samples is None:
            samples = bladeRF.ffi.new('int16_t[%s]' % (2 * num_samples))
        if self.module == bladeRF.MODULE_RX:
            func = bladeRF.rx
        else:
            func = bladeRF.tx
        func(self.raw_device, bladeRF.ffi.cast('void *', samples), num_samples, metadata, timeout_ms)
        return samples


class Device(object):

    def __init__(self, device_identifier=''):
        self._device = bladeRF.open(device_identifier)
        self.lock = RLock()

    @classmethod
    def from_params(cls, device_identifier='',
                    rx_frequency=1000000000, rx_bandwidth=7000000,
                    rx_sample_rate=10000000, tx_frequency=1000000000,
                    tx_bandwidth=7000000, tx_sample_rate=10000000):
        device = cls(device_identifier)
        if rx_frequency:
            device.rx.enabled = True
            device.rx.frequency = rx_frequency
            device.rx.bandwidth = rx_bandwidth
            device.rx.sample_rate = rx_sample_rate
        if tx_frequency:
            device.tx.enabled = True
            device.tx.frequency = tx_frequency
            device.tx.bandwidth = tx_bandwidth
            device.tx.sample_rate = tx_sample_rate
        return device

    @property
    def raw_device(self):
        return self._device[0]

    @property
    def rx(self):
        return Module(self, bladeRF.MODULE_RX)

    @property
    def tx(self):
        return Module(self, bladeRF.MODULE_TX)

    @property
    def fpga_size(self):
        return bladeRF.get_fpga_size(self.raw_device)

    @property
    def lna_gain(self):
        return bladeRF.get_lna_gain(self.raw_device)

    @lna_gain.setter
    def lna_gain(self, gain):
        return bladeRF.set_lna_gain(self.raw_device, gain)

    def __del__(self):
        bladeRF.close(self.raw_device)

