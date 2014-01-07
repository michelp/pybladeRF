import bladeRF

with bladeRF.open() as device:
    bladeRF.enable_module(device, bladeRF.MODULE_RX, True)
    print bladeRF.set_sample_rate(device, bladeRF.MODULE_RX, 2**20)
    print bladeRF.get_sample_rate(device, bladeRF.MODULE_RX)

