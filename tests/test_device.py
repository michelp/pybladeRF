import bladeRF


def test_device():
    device = bladeRF.Device()
    device.rx.config(bladeRF.FORMAT_SC16_Q11, 64, 16384, 16, 3500)
    device.tx.config(bladeRF.FORMAT_SC16_Q11, 64, 16384, 16, 3500)
    device.rx.enabled = True
    device.tx.enabled = True

    device.rx.frequency = 2**28
    assert device.rx.frequency == 2**28
    device.rx.bandwidth = 1500000
    assert device.rx.bandwidth == 1500000
    device.rx.sample_rate = 2**21
    assert device.rx.sample_rate == 2**21

    device.tx.frequency = 1234000000
    assert device.tx.frequency == 1234000000
    device.tx.bandwidth = 1500000
    assert device.tx.bandwidth == 1500000
    device.tx.sample_rate = 2**20
    assert device.tx.sample_rate == 2**20

    raw = device.rx(1024)
    array = bladeRF.samples_to_narray(raw, 1024)
    assert len(array) == 1024
    samples = bytearray(bladeRF.ffi.buffer(raw))
    assert isinstance(samples, bytearray)
    assert len(samples) == 4096

    device.tx(1024, raw)
