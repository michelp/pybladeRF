import bladeRF


class Module(object):

    def __init__(self, device, module):
        self.device = device
        self.module = module

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

