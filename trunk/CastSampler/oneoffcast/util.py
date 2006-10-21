#!/usr/bin/env python
#
# $Id$
#
# Copyright 2006 Doug Hellmann.
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

"""Utility functions.

"""

#
# Import system modules
#
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect


#
# Import Local modules
#
import logging

#
# Module
#

def ajaxErrorHandling():
    """Simple decorator to log and return error messages.
    """
    def decorator(func):

        def newfunc(*args, **kw):
            try:
                output = func(*args, **kw)
            except Exception, err:
                logging.exception(err)
                return HttpResponse('<div class="error">%s</div>' % err)
            return output
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator

def jsonView():
    """Simple decorator to convert the response to a json message.
    """
    def decorator(func):

        def newfunc(*args, **kw):
            try:
                output = func(*args, **kw)
                if not 'error' in output:
                    output['error'] = ''
            except Exception, err:
                logging.exception(err)
                output = { 'error':str(err) }
            json_response = simplejson.dumps(output)
            return HttpResponse(json_response)
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator

def jsonQuery():
    """Simple decorator to convert the response to a json message.
    """
    def decorator(func):

        def newfunc(*args, **kw):
            try:
                results = func(*args, **kw)
            except Exception, err:
                logging.exception(err)
                output = { 'error':str(err),
                           }
                json_response = simplejson.dumps(output)
            else:
                json_response = serializers.serialize('json', results)
            return HttpResponse(json_response)
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator


def same_user_only():
    """Simple decorator to convert the response to a json message.
    """
    def decorator(func):

        def newfunc(request, username, *args, **kw):
            if request.user.username != username:
                raise RuntimeError('You are not allowed to see this page')
            output = func(request, username, *args, **kw)
            return output
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator
