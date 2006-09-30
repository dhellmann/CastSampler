#
# $Id$
#

from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    # Example:
    # (r'^OneOffCast/', include('OneOffCast.apps.foo.urls.foo')),
    
    # Main page
    (r'^$', 'oneoffcast.views.main'),
    
    # Override the URL for blind logins to take the user to their home page
    (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url':'/cast/'}),
    # Account registration, login, etc.
    (r'^accounts/', include('registration.urls')),
    
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    # The oneoffcast app
    (r'^cast/', include('oneoffcast.urls')),

    # Static content (CSS, images, etc.)
    (r'^static/(.*)$', 'django.views.static.serve',
     { 'document_root':'/Users/dhellmann/Devel/OneOffCast/src/trunk/OneOffCast/static'}),

)
