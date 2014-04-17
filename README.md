pybladeRF
=========

Python CFFI wrapper around libbladeRF


Install
=======

To start you'll need to have build and installed libbladeRF.  See the
nuand docs for that.   You'll need a device too.

On ubuntu, you'll need some packages to build pybladeRF:

  python-dev libffi-dev python-virtualenv

Source the 'bootstrap' script to create a local virtual environment
where you can use the library.

If you want to run the tests, do 'python setup.py test'

See the tests directory for some example usage of the python API.


Tools
=====

The pybladeRF package installs some command line tools.

  pyblade-rx:  An I/Q receiver, writes to file or stdout

  pyblade-tx: An I/Q transmitter, reads from file or stdin

  pyblade-repeater:  A repeater, everything that is received is retransmitted.

  Check out the tools package for source code, all 3 programs use the
  asynchronous streaming API.
