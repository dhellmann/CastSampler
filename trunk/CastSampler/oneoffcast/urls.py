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
from oneoffcast import feeds


#
# Module
#

feeds = {
    'atom':feeds.AtomFeed,
    'rss':feeds.RSSFeed,
    }

urlpatterns = patterns(
    '',
    # User feed
    (r'^feed/(?P<url>.*)$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    ) + \
            patterns('oneoffcast.views',

    # Process access to external feeds
    (r'^external/(?P<id>\d+)', 'external'),

    # AJAX calls for user page
    (r'^(?P<username>[^/]+)/queue/(?P<id>\d+)/$', 'remove_from_queue'),
    (r'^(?P<username>[^/]+)/queue/$', 'queue'),
    (r'^(?P<username>[^/]+)/feed_list/$', 'feed_list'),

    # Subscriptions to podcasts
    (r'^(?P<username>[^/]+)/subscriptions/((?P<feed_id>\d+)/)?$', 'subscriptions'),

    # User pages
    (r'^(?P<username>[^/]+)/$', 'user'),

    # No user specified, try to determine from the session
    (r'^$', 'user_redirect'),
    )
