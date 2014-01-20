from threading import Thread
from time import sleep
import bladeRF


class Stream(Thread):

    def __init__(self, device, module, callback,
                 num_buffers, format, num_samples,
                 num_transfers, user_data=None):
        print user_data
        Thread.__init__(self)
        self.device = device
        self.module = module
        self.callback = callback
        self.user_data_handle = bladeRF.ffi.new_handle(user_data)
        self.stream, self.buffers = bladeRF.init_stream(
            self.device, callback, num_buffers, format,
            num_samples, num_transfers, self.user_data_handle)

    def run(self):
        bladeRF.stream(self.stream, self.module)


class Module(object):

    def __init__(self, device, module):
        self.device = device
        self.module = module

    def __call__(self, *args, **kwargs):
        if self.module == bladeRF.MODULE_RX:
            return bladeRF.rx(self.device, *args, **kwargs)
        elif self.module == bladeRF.MODULE_TX:
            return bladeRF.tx(self.device, *args, **kwargs)

    @property
    def enabled(self):
        return bladeRF.enable_module(self.device, self.module, True)

    @enabled.setter
    def enabled(self, enabled):
        bladeRF.enable_module(self.device, self.module, enabled)

    @property
    def frequency(self):
        return bladeRF.get_frequency(self.device, self.module)

    @frequency.setter
    def frequency(self, frequency):
        bladeRF.set_frequency(self.device, self.module, frequency)

    @property
    def bandwidth(self):
        return bladeRF.get_bandwidth(self.device, self.module)

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        bladeRF.set_bandwidth(self.device, self.module, bandwidth)

    @property
    def sample_rate(self):
        return bladeRF.get_sample_rate(self.device, self.module)

    @sample_rate.setter
    def sample_rate(self, sample_rate):
        bladeRF.set_sample_rate(self.device, self.module, sample_rate)

    @property
    def transfer_timeout(self):
        return bladeRF.get_transfer_timeout(self.device, self.module)

    @transfer_timeout.setter
    def transfer_timeout(self, timeout):
        bladeRF.set_transfer_timeout(self.device, self.module, timeout)

    def stream(self, callback, num_buffers, format, num_samples,
               num_transfers, user_data=None):
        print user_data
        return Stream(self.device, self.module, callback,
                      num_buffers, format, num_samples,
                      num_transfers, user_data=user_data)
        


class Device(object):

    def __init__(self, device_identifier=''):
        self._device = bladeRF.open(device_identifier)

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
    def device(self):
        return self._device[0]

    @property
    def rx(self):
        return Module(self.device, bladeRF.MODULE_RX)

    @property
    def tx(self):
        return Module(self.device, bladeRF.MODULE_TX)

    def __del__(self):
        bladeRF.close(self.device)

