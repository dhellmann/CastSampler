#
# Copyright (c) 2006 Racemi, Inc.  All rights reserved.
#

"""Various form manipulators

"""

_module_id_ = '$Id$'

#
# Import system modules
#
from django import forms
import feedparser
import logging

#
# Import Local modules
#
from oneoffcast.models import Podcast

#
# Module
#

class ShowFeedContentsForm(forms.Manipulator):
    """Define the elements of the form we use to
    show the contents of a feed (user submits URL).
    """

    def __init__(self):
        self.fields = (
            forms.URLField(field_name='url',
                           is_required=True,
                           ),
            )
        return

    def save(self, new_data):
        url = new_data['url']
        
        #
        # Do we already know about the feed?
        #
        logging.debug('checking for existing podcast')
        existing_casts = Podcast.objects.filter(feed_url=url)
        if existing_casts.count() > 0:
            podcast = existing_casts[0]
            logging.debug('found existing podcast')

            data = feedparser.parse(url)
            
        else:
            logging.debug('parsing %s' % url)
            data = feedparser.parse(url)

            name = data.feed.title
            description = data.feed.description
            home_url = data.feed.link
            
            podcast = Podcast(name=name,
                              description=description,
                              home_url=home_url,
                              feed_url=url,
                              )
            podcast.save()
        return podcast, data
