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

basic_feeds = {
    # User's queue
    'rss':feeds.RSSFeed,
    # Monitor a podcast
    'monitor':feeds.ProxyFeed,
    }


feed_patterns = patterns(
    'django.contrib.syndication.views',
    # User feed
    (r'^feed/(?P<url>.*)$', 'feed', {'feed_dict': basic_feeds}),
             
    )

view_patterns = patterns(
    'oneoffcast.views',
    
    # Process access to external feeds
    (r'^external/(?P<id>\d+)', 'external'),
    
    # AJAX calls for user page
    (r'^(?P<username>[^/]+)/queue/(?P<id>\d+)/$', 'remove_from_queue'),
    (r'^(?P<username>[^/]+)/queue/$', 'queue'),

    # Links from the monitor feed
    (r'^(?P<username>[^/]+)/add_to_queue/$', 'add_to_queue'),
    
    # Subscriptions to podcasts
    (r'^(?P<username>[^/]+)/subscriptions/((?P<feed_id>\d+)/)?$', 'subscriptions'),
    
    # User pages
    (r'^(?P<username>[^/]+)/$', 'user'),
    
    # No user specified, try to determine from the session
    (r'^$', 'user_redirect'),
    )

urlpatterns = feed_patterns + view_patterns
