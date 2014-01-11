import bladeRF


def test_init():

    with bladeRF.open_device() as device:
        bladeRF.enable_module(device, bladeRF.MODULE_RX, True)
        rate = 2**20
        bladeRF.set_sample_rate(device, bladeRF.MODULE_RX, rate)
        assert bladeRF.get_sample_rate(device, bladeRF.MODULE_RX) == rate

        bw = 1500000
        bladeRF.set_bandwidth(device, bladeRF.MODULE_RX, bw)
        assert bladeRF.get_bandwidth(device, bladeRF.MODULE_RX) == bw

        freq = 2**28
        bladeRF.set_frequency(device, bladeRF.MODULE_RX, freq)
        assert bladeRF.get_frequency(device, bladeRF.MODULE_RX) == freq

        samples = bladeRF.rx(device, bladeRF.FORMAT_SC16_Q12, 1024)
        assert isinstance(samples, bytearray)
        assert len(samples) == 4096
