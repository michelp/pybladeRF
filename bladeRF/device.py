import bladeRF


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


class Device(object):

    def __init__(self, device_identifier=''):
        self._device = bladeRF.open(device_identifier)

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

