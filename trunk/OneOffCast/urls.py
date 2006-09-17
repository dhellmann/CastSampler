#
# $Id$
#

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^OneOffCast/', include('OneOffCast.apps.foo.urls.foo')),

    # Main page
    (r'^$', 'OneOffCast.oneoffcast.views.main'),
    
    # User registration
    (r'^accounts/register/$', 'OneOffCast.registration.views.register'),
    (r'^accounts/confirm/(?P<activation_key>.*)/$', 'OneOffCast.registration.views.confirm'),
    
    # User login
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/profile/$', 'OneOffCast.oneoffcast.views.login_redirect'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    
    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),

    # The oneoffcast app
    (r'^cast/', include('OneOffCast.oneoffcast.urls')),
)
