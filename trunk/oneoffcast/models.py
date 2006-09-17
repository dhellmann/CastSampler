#
# $Id$
#

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Podcast(models.Model):
    """A pointer to a podcast feed.
    """
    
    # These are the public fields which we will expose to the
    # end user in some way.
    name = models.CharField(maxlength=256)
    description = models.TextField(blank=True)
    home_url = models.URLField(blank=True)
    feed_url = models.URLField()
    registration_date = models.DateTimeField('date registered')

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
    enclosure = models.URLField()
