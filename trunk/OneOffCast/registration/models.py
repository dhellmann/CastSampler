#
# $Id$
#
"""User registration

based on http://www.b-list.org/weblog/2006/09/02/django-tips-user-registration
"""

from django.db import models

from django.contrib.auth.models import User 

class UserProfile(models.Model): 
    """Information about a user who is trying to register.
    """
    user = models.OneToOneField(User) 
    activation_key = models.CharField(maxlength=40) 
    key_expires = models.DateTimeField() 
    
    class Admin:
        list_display = ('user', 'key_expires')
        list_filter = ['key_expires']
        search_fields = ['user']
        date_hierarchy = 'key_expires'