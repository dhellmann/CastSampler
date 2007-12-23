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
import logging


#
# Import Local modules
#
from oneoffcast.download_cache import retrieve_feed

#
# Module
#

# Our logger
logger = logging.getLogger('oneoffcast.models')

class Podcast(models.Model):
    """A pointer to a podcast feed.
    """
    
    # These are the public fields which we will expose to the
    # end user in some way.
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    home_url = models.URLField(blank=True)
    feed_url = models.URLField()
    registration_date = models.DateTimeField('date registered', auto_now_add=True)

    # Associate podcasts with users
    users = models.ManyToManyField(User)

    # These fields are only visible in the admin screens
    # and are used to control whether or not the feed
    # should be ignored so users cannot add items from it.
    contact_name = models.CharField(max_length=128, blank=True)
    contact_email = models.EmailField(max_length=128, blank=True)
    notes = models.TextField(blank=True)
    allowed = models.BooleanField(default=True, blank=True)
    
    class Admin:
        fields = ( ('Basics', {'fields':('name', 'description', 'registration_date'),
                               }),
                   ('URLs', {'fields':('home_url', 'feed_url'),
                             }),
                   ('Allowed', {'fields':('notes', 'allowed',
                                          'contact_name', 'contact_email',
                                          ),
                               'classes':'collapse',
                               }),
                   ('Users', {'fields':('users',),
                              'classes':'collapse',
                              }),
                   )
        list_display = ('name', 'feed_url', 'allowed')
        list_filter = ['registration_date']
        search_fields = ['name', 'description', 'contact_name', 'contact_email', 'notes']
        date_hierarchy = 'registration_date'

    def __str__(self):
        return self.name

    def get_current_feed_contents(self):
        """Return the parsed feed data.
        """
        contents = retrieve_feed(self.feed_url)
        logger.debug('returning contents')
        return contents

    def get_use_count(self):
        """Returns the number of QueueItems referencing this podcast.
        """
        return QueueItem.objects.count(podcast=self)

    def as_dict(self, user):
        """Return a dictionary of interesting values that the view
        wants, in a form suitable for serializing via JSON.
        """
        d = { 'name':self.name,
              'home_url':self.home_url,
              'feed_url':self.feed_url,
              'id':self.id,
              }
        return d

def find_or_create_podcast(feed_url, user=None):
    """Look for an existing Podcast with the given
    feed_url.  If not found create it.  Return the
    Podcast and a feedparser version of the parsed
    feed.
    """
    #
    # Do we already know about the feed?
    #
    logger.debug('checking for existing podcast')
    existing_casts = Podcast.objects.filter(feed_url=feed_url)
    if existing_casts.count() > 0:
        podcast = existing_casts[0]
        logger.debug('found existing podcast')
        data = podcast.get_current_feed_contents()

    else:
        logger.debug('creating podcast from feed %s', feed_url)
        data = retrieve_feed(feed_url)
        #logger.debug(data)

        try:
            name = data.feed.title.encode('utf-8', 'replace')
        except AttributeError, err:
            logger.debug('data is a %s', data.__class__.__name__)
            logger.debug(data)
            raise RuntimeError('Could not parse %s: %s' % (feed_url, 'no title'))
        try:
            description = data.feed.description.encode('utf-8', 'replace')
        except AttributeError, err:
            description = ''
        try:
            home_url = data.feed.link.encode('utf-8', 'replace')
        except AttributeError, err:
            raise RuntimeError('Could not parse %s: %s' % (feed_url, 'no site URL'))
        
        podcast = Podcast(name=name,
                          description=description,
                          home_url=home_url,
                          feed_url=feed_url,
                          )
        podcast.save()

    #
    # Make sure the feed is assciated with the user
    #
    if user is not None:
        podcast.users.add(user)

    return podcast, data
    

class QueueItem(models.Model):
    """Items in a user's queue.
    """
    user = models.ForeignKey(User)
    podcast = models.ForeignKey(Podcast)
    title = models.CharField(max_length=512, blank=True)
    summary = models.TextField(blank=True)
    link = models.URLField(verify_exists=False)
    item_enclosure_url = models.URLField(verify_exists=False)
    item_enclosure_length = models.IntegerField()
    item_enclosure_mime_type = models.CharField(max_length=200)
    add_date = models.DateTimeField('date added', auto_now_add=True)
    author_name = models.CharField(max_length=128, blank=True)
    author_email = models.EmailField(max_length=128, blank=True)

    class Admin:
        fields = ( ('Owner', {'fields':('user', 'add_date'),
                              }),
                    ('Podcast', {'fields':('podcast', ),
                               }),
                   ('Item', {'fields':('title', 
                                       'summary', 
                                       'link',
                                       'author_name',
                                       'author_email',
                                       'item_enclosure_url',
                                       'item_enclosure_length', 
                                       'item_enclosure_mime_type',
                                       ),
                             }),
                   )
        list_display = ('title', 'link', 'user', 'add_date', 'podcast')
        list_filter = ['add_date', 'podcast', 'user']
        search_fields = ['title', 'summary']
        date_hierarchy = 'add_date'
    
    def get_absolute_url(self):
        "Used in feed generation."
        return self.link
    
    def get_truncated_summary(self, maxLen=30):
        "Return a shorter version of the text in the summary."
        desc = self.summary
        if len(desc) > maxLen:
            desc = desc[:maxLen] + ' ...'
        return desc

    def as_dict(self):
        """Return a dictionary of interesting values that the view
        wants, in a form suitable for serializing via JSON.
        """
        d = { 'podcast_name':self.podcast.name,
              'podcast_home':self.podcast.home_url,
              'title':self.title,
              'link':self.link,
              'truncated_summary':self.get_truncated_summary(),
              'summary':self.summary,
              'enclosure_url':self.item_enclosure_url,
              'enclosure_mimetype':self.item_enclosure_mime_type,
              'pubdate':self.add_date.ctime(),
              'id':self.id,
              }
        return d
