#
# $Id$
#

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^OneOffCast/', include('OneOffCast.apps.foo.urls.foo')),

    # Main page
    (r'^$', 'OneOffCast.oneoffcast.views.main'),
    
    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),

    # The oneoffcast app
    (r'^cast/', include('OneOffCast.oneoffcast.urls')),
)
