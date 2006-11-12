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

"""User registration

based on http://www.b-list.org/weblog/2006/09/02/django-tips-user-registration

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


urlpatterns = patterns('registration.views',

    # User registration
    (r'^register/$', 'register'),
    (r'^confirm/(?P<activation_key>.*)/$', 'confirm'),

) + patterns('django.contrib.auth.views',
    # User login and logout
    (r'^login/$', 'login', {'template_name':'login.html'}),
    (r'^logout/$', 'logout', {'next_page':'/'}),
    )
