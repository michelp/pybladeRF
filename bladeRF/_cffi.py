import os
import inspect
from functools import wraps
from cffi import FFI

lib = None
ffi = FFI()

ffi.cdef("""
#define BLADERF_ERR_UNEXPECTED ...
#define BLADERF_ERR_RANGE ...
#define BLADERF_ERR_INVAL ...
#define BLADERF_ERR_MEM ...
#define BLADERF_ERR_IO ...
#define BLADERF_ERR_TIMEOUT ...
#define BLADERF_ERR_NODEV ...
#define BLADERF_ERR_UNSUPPORTED ...
#define BLADERF_ERR_MISALIGNED ...
#define BLADERF_ERR_CHECKSUM ...
""")

# Code copied from michelp/pyczmq which was authored by me -mp

def ptop(typ, val=ffi.NULL):
    ptop = ffi.new('%s*[1]' % typ)
    ptop[0] = val
    return ptop


def cdef(decl, returns_string=False, nullable=False):
    ffi.cdef(decl)
    def wrap(f):
        @wraps(f)
        def inner_f(*args):
            val = f(*args)
            if nullable and val == ffi.NULL:
                return None
            elif returns_string:
                return ffi.string(val)
            return val

        # this insanity inserts a formatted argspec string
        # into the function's docstring, so that sphinx
        # gets the right args instead of just the wrapper args
        args, varargs, varkw, defaults = inspect.getargspec(f)
        defaults = () if defaults is None else defaults
        defaults = ["\"{}\"".format(a) if type(a) == str else a for a in defaults]
        l = ["{}={}".format(arg, defaults[(idx+1)*-1])
             if len(defaults)-1 >= idx else
             arg for idx, arg in enumerate(reversed(list(args)))]
        if varargs:
            l.append('*' + varargs)
        if varkw:
            l.append('**' + varkw)
        doc = "{}({})\n\nC: ``{}``\n\n{}".format(f.__name__, ', '.join(reversed(l)), decl, f.__doc__)
        inner_f.__doc__ = doc
        return inner_f
    return wrap

