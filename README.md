pybladeRF
=========

Python CFFI wrapper around libbladeRF


Install
=======

Obviously to start you'll need to have build and installed libbladeRF.
See the nuand docs for that.  Next thing you'll need is a device.

On ubuntu, you'll need some packages to build pybladeRF:

  python-dev libffi-dev python-virtualenv

Source the 'bootstrap' script to create a local virtual environment
where you can use the library.

If you want to run the tests, 'pip install nose' in the virtual
environment, then run 'nosetests'.  You should see happy dots.

Usage
=====

Here's a brief example from a test:

    import bladeRF

    def test_device():
	device = bladeRF.Device()
	device.rx.enabled = True
	device.tx.enabled = True

	device.rx.frequency = 2**28
	assert device.rx.frequency == 2**28
	device.rx.bandwidth = 1500000
	assert device.rx.bandwidth == 1500000
	device.rx.sample_rate = 2**21
	assert device.rx.sample_rate == 2**21
	device.rx.transfer_timeout = 10000
	assert device.rx.transfer_timeout == 10000

	device.tx.frequency = 1234000000
	assert device.tx.frequency == 1234000000
	device.tx.bandwidth = 1500000
	assert device.tx.bandwidth == 1500000
	device.tx.sample_rate = 2**20
	assert device.tx.sample_rate == 2**20

	samples = device.rx(bladeRF.FORMAT_SC16_Q12, 1024)
	assert isinstance(samples, bytearray)
	assert len(samples) == 4096

	device.tx(bladeRF.FORMAT_SC16_Q12, samples, 1024)


