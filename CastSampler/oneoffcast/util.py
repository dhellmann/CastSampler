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
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect

import logging
import re
import time

#
# Import Local modules
#
import settings

#
# Module
#

# Our logger
logger = logging.getLogger('oneoffcast.util')

def ajaxErrorHandling():
    """Simple decorator to log and return error messages.
    """
    def decorator(func):

        def newfunc(*args, **kw):
            try:
                output = func(*args, **kw)
            except Exception, err:
                logger.exception(err)
                return HttpResponse('<div class="error">%s</div>' % err)
            return output
        
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
                logger.exception(err)
                output = { 'error':str(err) }
            json_response = simplejson.dumps(output)
            return HttpResponse(json_response)
        
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
                logger.exception(err)
                output = { 'error':str(err),
                           }
                json_response = simplejson.dumps(output)
            else:
                json_response = serializers.serialize('json', results)
            return HttpResponse(json_response)
        
        newfunc.exposed = True
        return newfunc

    return decorator


def same_user_only():
    """Simple decorator to convert the response to a json message.
    """
    def decorator(func):

        def newfunc(request, username, *args, **kw):
            if request.user.username != username:
                from urllib import quote
                return HttpResponseRedirect('%s?%s=%s' % (settings.LOGIN_URL, REDIRECT_FIELD_NAME, quote(request.get_full_path())))
            output = func(request, username, *args, **kw)
            return output
        
        newfunc.exposed = True
        return newfunc

    return decorator

def convert_feed_to_entries(parsed_feed):
    """Process the entries in the feed and return
    a sequence of dictionaries with interesting
    values.
    """
    entries = []
    for e in parsed_feed['entries']:
        new_entry = {}
        new_entry.update(e)

        for name in [ 'summary_detail', 'title_detail', 'updated_parsed' ]:
            if name in new_entry:
                del new_entry[name]

        for attr in [ 'title', 'summary' ]:
             try:
                  stripped = strip_html(new_entry[attr])
             except KeyError:
                  continue
             encoded = stripped.encode('utf-8', 'replace')
             new_entry[attr] = encoded
             
        if new_entry.get('enclosures'):
            entries.append(new_entry)
        #logger.debug(new_entry)
    return entries


##
# Removes HTML markup from a text string.
#
# @param text The HTML source.
# @return The plain text.  If the HTML source contains non-ASCII
#     entities or character references, this is a Unicode string.
def strip_html(text):
    """Removes HTML markup from a text string.
    
    From http://effbot.org/zone/re-sub.htm#strip-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import htmlentitydefs
            entity = htmlentitydefs.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return unicode(entity, "iso-8859-1")
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)
