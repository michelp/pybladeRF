import bladeRF


def test_init():

    with bladeRF.open_device() as device:
        bladeRF.enable_module(device, bladeRF.MODULE_RX, True)
        bladeRF.sync_config(device, bladeRF.MODULE_RX, bladeRF.FORMAT_SC16_Q12,
                            64, 16384, 16, 3500)
        rate = 2**20
        bladeRF.set_sample_rate(device, bladeRF.MODULE_RX, rate)
        assert bladeRF.get_sample_rate(device, bladeRF.MODULE_RX) == rate

        bw = 1500000
        bladeRF.set_bandwidth(device, bladeRF.MODULE_RX, bw)
        assert bladeRF.get_bandwidth(device, bladeRF.MODULE_RX) == bw

        freq = 2**28
        bladeRF.set_frequency(device, bladeRF.MODULE_RX, freq)
        assert bladeRF.get_frequency(device, bladeRF.MODULE_RX) == freq

        num_samples = 1024
        raw = bladeRF.ffi.new('int16_t[%s]' % (2 * num_samples))
        bladeRF.rx(device, bladeRF.ffi.cast('void *', raw), num_samples, bladeRF.ffi.NULL, 0)

        samples = bytearray(bladeRF.ffi.buffer(raw))
        assert isinstance(samples, bytearray)
        assert len(samples) == 4096
