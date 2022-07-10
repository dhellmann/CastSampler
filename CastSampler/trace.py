#
# $Id$
#
# Copyright 2001 Doug Hellmann.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of Doug
# Hellmann not be used in advertising or publicity pertaining to
# distribution of the software without specific, written prior
# permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
# NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

"""A debugging trace module.

  This debugging trace module makes it easier to follow nested calls
  in output by varying the indention level for log messages.  The
  caller can simply trace 'into()' a new level when control passes
  into a function call, 'write()' debug messages at appropriate spots
  in the function, then call 'outof()' when returning from the
  function.

  The debug level is set via the environment variable 'TRACE_LEVEL'.
  Level '0' or no value specified results in no output.  Positive
  integer values are used to control the verbosity of the output with
  higher numbers resulting in more output messages.

"""

__rcs_info__ = {
    #
    #  Creation Information
    #
    'module_name'  : '$RCSfile$',
    'rcs_id'       : '$Id$',
    'creator'      : 'Doug Hellmann',
    'project'      : 'HappyDoc',
    'created'      : 'Mon, 29-Oct-2001 09:29:22 EST',

    #
    #  Current Information
    #
    'author'       : '$Author$',
    'version'      : '$Revision$',
    'date'         : '$Date$',
}
try:
    __version__ = __rcs_info__['version'].split(' ')[1]
except:
    __version__ = '0.0'

#
# Import system modules
#
import logging
import os
import pprint
try:
    from cStringIO import StringIO
except:
    import StringIO
import sys
import thread
import time

#
# Import Local modules
#

#
# Module
#

logger = logging.getLogger('trace')

class LogOutput:

    def write(self, msg):
        logger.debug(msg.rstrip('\n'))
        return
    

class DebugTracer:

    NO_RETURN_VALUE_SPECIFIED='No return value specified.'

    def __init__(self,
                 outputStream=None,
                 indentBy='  ',
                 maxOutputLevel=1,
                 startLevel=0,
                 tabSize=2):
        self.setOutputStream(outputStream)
        self.start_level = startLevel
        self.level = startLevel
        self.stack = ()
        self.setIndentBy(indentBy)
        self.max_output_level = maxOutputLevel
        self.setTabSize(tabSize)
        self.timer_info = {}
        return

    def setOutputStream(self, outputStream):
        """Set the destination for trace messages.

        The outputStream must support write() and flush() methods.
        """
        self.output = outputStream
        return

    def setIndentBy(self, indentBy):
        """Set the string to use for each indention level.
        """
        self.indent_by = indentBy
        return

    def setTabSize(self, tabSize):
        """Set the number of times the indentBy string should be
        printed for each indention level.
        """
        self.tab_size = tabSize
        return
    
    def setVerbosity(self, level):
        """Set the level of trace output.

        Higher levels include more output.
        """
        self.max_output_level = level
        return

    def getIndent(self, level=None):
        """Gets the indent string for the current level.
        """
        if level is None:
            level = self.level
        return self.indent_by * level

    def pushLevel(self, newStackTop):
        """Enter a new block, and increase the level setting.
        """
        self.level = self.level + 1
        self.stack = ( newStackTop, self.stack )
        return

    def popLevel(self):
        """Leave the current block, and decrease the level setting.
        """
        self.level = self.level - 1
        if self.stack:
            popped, self.stack = self.stack
        else:
            popped = ()
        #
        # Just in case the caller messes up.
        #
        if self.level < 0:
            self.level = 0
        return popped

    def clear(self):
        """Clear any existing levels.

        This is most useful for tests, where it would be desirable to
        ignore the fact that errors might disrupt the orderly
        arrangement of trace messages.
        """
        self.level = self.start_level
        self.stack = ()
        return

    def checkOutputLevel(self, outputLevel):
        return self.max_output_level >= outputLevel

    ###

    def into(_self, className, functionName, outputLevel=1, **params):
        """Enter a new debug trace level.
        
        Parameters

            'className' -- Name of the class.

            'functionName' -- The name of the function/method.

            'outputLevel=1' -- The debug level where this message should be printed.

            '**params' -- Parameters sent to the function.
        
        """
        if _self.checkOutputLevel(outputLevel):
            _self.write('%s::%s (' % (className, functionName))
            params = params.items()
            params.sort()
            tab = _self.indent_by * _self.tab_size
            for name, value in params:
                _self.write('%s%s=%s, ' % ( tab,
                                           name,
                                           repr(value),
                                           )
                           )
            _self.write('%s) {' % tab)
            start_time = time.time()
            _self.pushLevel((className, functionName, start_time))
        return

    def callerParent(self, outputLevel=1):
        if self.checkOutputLevel(outputLevel):
            if not self.stack:
                self.write('ERROR: trace.callerParent called when no stack present\n')
            if len(self.stack) < 2:
                parent = 'None'
            else:
                try:
                    parent = '%s::%s' % self.stack[1][0]
                except:
                    parent = str(self.stack[1])

            #self.output.write('Called by: %s\n' % parent)
            self.write('Called by: %s\n' % str(self.stack))
        return

    def timestamp(self, outputLevel=1):
        """Show the current timestamp.
        """
        if self.checkOutputLevel(outputLevel):
            time_stamp = time.asctime()
            self.write('Time-stamp: <%s>' % time_stamp, outputLevel=outputLevel)
        return

    def startTimer(self, timerName):
        timer_info = self.timer_info.setdefault(timerName, {})
        timer_info['start'] = time.time()
        return

    def endTimer(self, timerName):
        timer_info = self.timer_info[timerName]
        timer_info['end'] = time.time()
        return

    def elapsedTime(self, timerName, outputLevel=1):
        timer_info = self.timer_info[timerName]
        start = timer_info['start']
        end = timer_info['end']
        elapsed_seconds = end - start
        self.write('%s elapsed %s seconds' % (timerName, elapsed_seconds),
                   outputLevel=outputLevel,
                   )
        return

    def write(self, message, indent=1, outputLevel=1, includeNewline=1, **vars):
        if self.checkOutputLevel(outputLevel):
            
            if indent:
                prefix = self.getIndent()
            else:
                prefix = ''

            if self.output:
                output = self.output
            else:
                output = sys.stdout

            if includeNewline:
                newline = '\n'
            else:
                newline = ''

            if TRACE_SHOW_THREADS:
                output.write('[%s] ' % thread.get_ident())
            output.write('%s%s%s' % (prefix, message, newline))
            
            if vars.items():
                self.writeVar(**vars)
                
            if hasattr(output, 'flush'):
                output.flush()
        return

    def writeVar(self, outputLevel=1, **variables):
        if self.checkOutputLevel(outputLevel):

            if self.output:
                output = self.output
            else:
                output = sys.stdout
                
            prefix = self.getIndent()
            tab = self.indent_by * self.tab_size
            
            variables = variables.items()
            variables.sort()
            for name, value in variables:
                if TRACE_SHOW_THREADS:
                    output.write('[%s] ' % thread.get_ident())
                output.write('%s%s%s=' % (prefix,
                                          tab,
                                          name,
                                          )
                             )
                
                #
                # Format the value of the variable
                # nicely.
                #
                value_prefix = self.getIndent(self.level + 1) + (' ' * (len(name) + 2))
                value_buffer = StringIO()
                pprint.pprint(value, value_buffer)
                value_text = value_buffer.getvalue()
                value_lines = value_text.split('\n')

                output.write('%s\n' % value_lines[0])

                for vl in value_lines[1:-1]:
                    if TRACE_SHOW_THREADS:
                        output.write('[%s] ' % thread.get_ident())
                    output.write('%s%s\n' % (value_prefix,
                                             vl,
                                             )
                                 )

                #
                # pprint may add an extra newline, so
                # only print the last line if it is
                # not just whitespace
                #
                if ( (len(value_lines) > 1)
                     and
                     value_lines[-1].strip()
                     ):
                    if TRACE_SHOW_THREADS:
                        output.write('[%s] ' % thread.get_ident())
                    output.write('%s%s' % (value_prefix,
                                           value_lines[-1],
                                           )
                                 )
        return

    def outof(self, returnValue=None, outputLevel=1):
        """Exit the current debug trace level.
        
            Parameters

              'returnValue' -- Optional argument indicating
                               the value returned from the function.
        """
        if self.checkOutputLevel(outputLevel):
            try:
                class_name, function_name, start_time = self.popLevel()
            except ValueError:
                # Someone screwed up the trace stack, so
                # the tuple didn't unpack correctly.
                start_time = time.time()
                #raise
            end_time = time.time()
            #
            # Compute elapsed second, rounding up to nearest thousandth.
            #
            elapsed_seconds = (end_time + 0.0005) - start_time
            self.write('} (%4.3f sec) %s' % (elapsed_seconds, repr(returnValue)))
        return returnValue

    def showTraceback(self, outputLevel=1):
        """Print the traceback for the current exception.
        """
        if self.checkOutputLevel(outputLevel):
            import traceback
            traceback.print_exc()
        return

TRACE_SHOW_THREADS = int(os.environ.get('TRACE_THREADS', 0))
GLOBAL_TRACE_LEVEL = int(os.environ.get('TRACE_LEVEL', 0))
trace=DebugTracer(maxOutputLevel=GLOBAL_TRACE_LEVEL)
into=trace.into
outof=trace.outof
write=trace.outof

##################################################################
#
# decorators and decorator factories
#
##################################################################
import types
import inspect
import decotools 
def tracelevel(level=1): # {
    """Create a tracing decorator that traces at the specified level.
    If GLOBAL_TRACE_LEVEL is zero, then generates a noop decorator
    that simply returns the same function.
    """
    # this function, a decorator factory, runs at import/definition time
    if GLOBAL_TRACE_LEVEL < level:
        return decotools.noopdeco
    else:
        def deco(f):
            cframe = sys._getframe(2) # the original caller of the decorator
            _callername = cframe.f_code.co_name
            _args, _varargs, _varkw, _defaults = inspect.getargspec(f)
            _fname = f.__name__
            _func_code = f.func_code
            if _defaults:
                _firstdefault = len(_args) - len(_defaults)

            # stuff out here happens at import/definition time
            
            def _dynacenter_tracer_(*args, **kwds): # {
                # stuff in here happens at runtime
                numargs = len(args)
                params = {}
                for i, name in enumerate(_args):
                    if i < numargs:
                        params[ name ] = args[i]
                    elif _defaults and i >= _firstdefault:
                        params[ name ] = _defaults[ i - _firstdefault ]
                # now override defaults w/ what we got in kwds
                params.update(kwds)

                params['className']    = _callername
                params['functionName'] = _fname
                params['outputLevel']  = level

                rc = None # define this here for outof in case f raises
                into( **params )
                try:
                    rc = f( *args, **kwds )
                except Exception, err:
                    outof( returnValue = err, outputLevel = level )
                    raise
                else:
                    outof( returnValue = rc, outputLevel = level )

                return rc
            # } def _dynacenter_tracer_
            return _dynacenter_tracer_
        return decotools.functools_decorator(deco)
    return
# } def tracelevel

#TRACE_ALL_LEVEL    = 1000 # use this only on small unit tests
#TRACE_RACEMI_LEVEL = TRACE_ALL_LEVEL - 1
#if GLOBAL_TRACE_LEVEL >= TRACE_RACEMI_LEVEL:
# comment out the if False below and uncomment the three lines above to enable
if False:

    if GLOBAL_TRACE_LEVEL > TRACE_RACEMI_LEVEL:
        def getRacemiModule(filename):
            return filename # for everything (be careful)
    else:
        def getRacemiModule(filename):
            idx = filename.find('racemi')
            if idx >= 0:
                return filename[idx:]

    DebugTracerNames = dir(DebugTracer)

    from collections import deque
    import threading
    def defaultTracer(frame, event, arg):
        if event not in ('call', 'return'):
            # we'll get called for c_call and c_return among others
            # but we only care about call and return
            return defaultTracer

        t = threading.currentThread()
        try:
            _stack = t._stack
        except AttributeError:
            t._stack = deque()
            _stack = t._stack

        f_code = frame.f_code
        if event == 'call':

            func_name = f_code.co_name
            filename = getRacemiModule(f_code.co_filename)
            if filename and func_name not in DebugTracerNames:
                # figure out stuff we need to call the into() method
                params = dict(frame.f_locals)
                params['className'] = '%s:%s' % (filename, frame.f_lineno)
                params['functionName'] = func_name
                # 
                into( **params )
                # save this call so we know when to close it
                _stack.append(f_code)

        elif len(_stack) and event == 'return':

            if f_code == _stack.pop():
                outof( returnValue = arg )
            else:
                _stack.append(f_code)

        return defaultTracer

    threading.setprofile(defaultTracer)
    sys.setprofile(defaultTracer)
