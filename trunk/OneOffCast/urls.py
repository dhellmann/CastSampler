#
# $Id$
#

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^OneOffCast/', include('OneOffCast.apps.foo.urls.foo')),

    # Main page
    (r'^$', 'OneOffCast.oneoffcast.views.main'),

    # Override the URL for blind logins to take the user to their home page
    (r'^accounts/profile/$', 'OneOffCast.oneoffcast.views.login_redirect'),
    # Account registration, login, etc.
    (r'^accounts/', include('OneOffCast.registration.urls')),
    
    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),

    # The oneoffcast app
    (r'^cast/', include('OneOffCast.oneoffcast.urls')),
)
