pybladeRF
=========

Python CFFI wrapper around libbladeRF


Install
=======

Obviously to start you'll need to have build and installed libbladeRF.
See the nuand docs for that.  Next thing you'll need is a device.

On ubuntu, you'll need some packages to build pybladeRF:

  python-dev libffi-dev python-virtualenv

Source the 'bootstrap' script to create a local virtual environment.
Now you should be able to do:

  python test.py

if it returns no output, it worked!
