#
# $Id$
#

from django.conf.urls.defaults import *

#feeds = {
#    'user':
#    }

urlpatterns = patterns('',
    # Example:
    # (r'^OneOffCast/', include('OneOffCast.apps.foo.urls.foo')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
    
#    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
