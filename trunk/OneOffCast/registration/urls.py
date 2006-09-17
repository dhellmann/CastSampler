#
# $Id$
#

from django.conf.urls.defaults import *

urlpatterns = patterns('OneOffCast.registration.views',

    # User registration
    (r'^register/$', 'register'),
    (r'^confirm/(?P<activation_key>.*)/$', 'confirm'),

) + patterns('django.contrib.auth.views',
    # User login and logout
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    )