#!/usr/bin/env python
#
# $Id$
#
# Copyright 2006 Doug Hellmann.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of Doug
# Hellmann not be used in advertising or publicity pertaining to
# distribution of the software without specific, written prior
# permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
# NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

"""User registration

based on http://www.b-list.org/weblog/2006/09/02/django-tips-user-registration

"""

#
# Import system modules
#
from django.db import models

from django.contrib.auth.models import User 

#
# Import Local modules
#


#
# Module
#

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
