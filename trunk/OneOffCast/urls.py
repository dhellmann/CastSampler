#
# $Id$
#

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^OneOffCast/', include('OneOffCast.apps.foo.urls.foo')),

    # Main page
    (r'^$', 'OneOffCast.oneoffcast.views.main'),
    
    # User login
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    
    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),

    # The oneoffcast app
    (r'^cast/', include('OneOffCast.oneoffcast.urls')),
)
