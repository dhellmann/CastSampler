#
# $Id$
#

from django.conf.urls.defaults import *
from oneoffcast import feeds

feeds = {
    'atom':feeds.UserFeed,
    }

urlpatterns = patterns('',
    # User feed
    (r'^feed/(?P<url>.*)$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
) + \
            patterns('OneOffCast.oneoffcast.views',

    # User pages
    (r'^(?P<username>.*)/$', 'user'),
    )