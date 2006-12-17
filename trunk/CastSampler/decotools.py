#
# $Id$
#
# A collection of decorator tools
#
# This module might be dropped if the new python 2.5 functools module
# includes what we need.
#
# 

# null decorator
def noopdeco(func):
    return func

#######################################################################
#
# From the python decorator library

def simple_decorator(decorator):
    """This decorator can be used to turn simple functions
    into well-behaved decorators, so long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is 
    eligible to use this. Simply apply @simple_decorator to
    your decorator and it will automatically preserve the 
    docstring and function attributes of functions to which
    it is applied."""
    def new_decorator(f):
        g = decorator(f)
        g.__modules = f.__module__ # added by lpc
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    # Now a few lines needed to make simple_decorator itself
    # be a well-behaved decorator.
    new_decorator.__module = decorator.__module__ # added by lpc
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator

#######################################################################
#
# From the proposed functools module (May 2006)
#
def _update_wrapper(decorated, func, deco_func):
    # Support naive introspection
    decorated.__module__ = func.__module__
    decorated.__name__ = func.__name__
    decorated.__doc__ = func.__doc__
    decorated.__dict__.update(func.__dict__)

def functools_decorator(deco_func):
    """Wrap a function as an introspection friendly decorator function"""
    def wrapper(func):
        decorated = deco_func(func)
        if decorated is func:
            return func
        _update_wrapper(decorated, func, deco_func)
        return decorated
    # Manually make this decorator introspection friendly
    _update_wrapper(wrapper, deco_func, functools_decorator)
    return wrapper

# I tried the signature preserving decorator module written by
# Michele Simionato but it forced me to call inspect.getargspec
# at runtime instead of definition time.
