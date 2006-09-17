#
# $Id$
#

from django.conf.urls.defaults import *
from oneoffcast import feeds

feeds = {
    'atom':feeds.UserFeed,
    }

urlpatterns = patterns('',
    # Example:
    # (r'^OneOffCast/', include('OneOffCast.apps.foo.urls.foo')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
    
    # Main page
    (r'^$', 'OneOffCast.oneoffcast.views.main'),
    # User pages
    (r'^cast/(?P<user_id>.*)$', 'OneOffCast.oneoffcast.views.user'),
    # User feed
    (r'^feed/(?P<url>.*)$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
