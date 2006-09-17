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

"""

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

class Podcast(models.Model):
    """A pointer to a podcast feed.
    """
    
    # These are the public fields which we will expose to the
    # end user in some way.
    name = models.CharField(maxlength=256)
    description = models.TextField(blank=True)
    home_url = models.URLField(blank=True)
    feed_url = models.URLField()
    registration_date = models.DateTimeField('date registered', auto_now_add=True)

    # These fields are only visible in the admin screens
    # and are used to control whether or not the feed
    # should be ignored so users cannot add items from it.
    contact_name = models.CharField(maxlength=128, blank=True)
    contact_email = models.EmailField(maxlength=128, blank=True)
    notes = models.TextField(blank=True)
    ignore = models.BooleanField(default=False, blank=True)
    
    class Admin:
        fields = ( ('Basics', {'fields':('name', 'description', 'registration_date'),
                               }),
                   ('URLs', {'fields':('home_url', 'feed_url'),
                             }),
                   ('Ignore', {'fields':('contact_name', 'contact_email', 'notes', 'ignore'),
                               'classes':'collapse',
                               }),
                   )
        list_display = ('name', 'feed_url', 'ignore')
        list_filter = ['registration_date']
        search_fields = ['name', 'description', 'contact_name', 'contact_email', 'notes']
        date_hierarchy = 'registration_date'

    def __str__(self):
        return self.name

class QueueItem(models.Model):
    """Items in a user's queue.
    """
    user = models.ForeignKey(User)
    podcast = models.ForeignKey(Podcast)
    title = models.CharField(maxlength=512, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(verify_exists=False)
    item_enclosure_url = models.URLField(verify_exists=False)
    item_enclosure_length = models.IntegerField()
    item_enclosure_mime_type = models.CharField(maxlength=200)
    add_date = models.DateTimeField('date added', auto_now_add=True)

    class Admin:
        fields = ( ('Owner', {'fields':('user', 'add_date'),
                              }),
                    ('Podcast', {'fields':('podcast', ),
                               }),
                   ('Item', {'fields':('title', 
                                       'description', 
                                       'link',
                                       'item_enclosure_url',
                                       'item_enclosure_length', 
                                       'item_enclosure_mime_type'),
                             }),
                   )
        list_display = ('user', 'add_date', 'podcast', 'title')
        list_filter = ['add_date', 'podcast']
        search_fields = ['title', 'description']
        date_hierarchy = 'add_date'
    
    def get_absolute_url(self):
        "Used in feed generation."
        return self.link
    
