from threading import Thread, RLock
import weakref
import bladeRF


class Stream(Thread):

    def __init__(self, device, module, callback,
                 num_buffers, format, num_samples,
                 num_transfers, user_data=None):
        Thread.__init__(self)
        self.running = True
        self.current = 0
        self.num_buffers = num_buffers
        self.device = device
        self.module = module

        @bladeRF.ffi.callback('bladerf_stream_cb')
        def raw_callback(raw_device, raw_stream, meta, samples, num_samples, user_data):
            user_data = bladeRF.ffi.from_handle(user_data)
            v = callback(self.device, self, meta, samples, num_samples, user_data)
            if v is None:
                return bladeRF.ffi.NULL
            return v

        self.callback = callback
        self.raw_callback = raw_callback
        self.user_data_handle = bladeRF.ffi.new_handle(user_data)
        self.raw_stream, self.buffers = bladeRF.init_stream(
            self.device.raw_device, raw_callback, num_buffers, format,
            num_samples, num_transfers, self.user_data_handle)

    def next(self):
        if not self.running:
            return
        ret = self.buffers[self.current]
        self.current += 1
        if self.current >= self.num_buffers:
            self.current = 0
        return ret

    def run(self):
        bladeRF.stream(self.raw_stream, self.module)



class Module(object):

    def __init__(self, device, module):
        self.device = device
        self.raw_device = device.raw_device
        self.module = module

    def __call__(self, *args, **kwargs):
        if self.module == bladeRF.MODULE_RX:
            return bladeRF.rx(self.raw_device, *args, **kwargs)
        elif self.module == bladeRF.MODULE_TX:
            return bladeRF.tx(self.raw_device, *args, **kwargs)

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
    def transfer_timeout(self):
        return bladeRF.get_transfer_timeout(self.raw_device, self.module)

    @transfer_timeout.setter
    def transfer_timeout(self, timeout):
        bladeRF.set_transfer_timeout(self.raw_device, self.module, timeout)

    def stream(self, callback, num_buffers, format, num_samples,
               num_transfers, user_data=None):
        return Stream(self, self.module, callback,
                      num_buffers, format, num_samples,
                      num_transfers, user_data=user_data)
        


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

