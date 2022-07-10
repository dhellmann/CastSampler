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

"""

"""

#
# Import system modules
#
from django.conf.urls.defaults import *


#
# Import Local modules
#


#
# Module
#


urlpatterns = patterns(
    '',
    # Example:
    # (r'^CastSampler/', include('CastSampler.apps.foo.urls.foo')),
    
    # Main page
    (r'^$', 'views.main'),
    
    # Override the URL for blind logins to take the user to their home page
    (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url':'/cast/'}),
    # Account registration, login, etc.
    (r'^accounts/', include('registration.urls')),
    
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    # The oneoffcast app
    (r'^cast/', include('oneoffcast.urls')),

    # Static content (CSS, images, etc.)
    (r'^static/(.*)$', 'django.views.static.serve',
     { 'document_root':'/Users/dhellmann/Devel/CastSampler/src/trunk/CastSampler/static'}),

    # Contact page and user feedback form
    (r'^contact/$', 'views.contact'),
)
