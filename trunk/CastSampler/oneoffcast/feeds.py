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

"""Feed generation

"""

#
# Import system modules
#
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed, add_domain
from django.utils.feedgenerator import Rss201rev2Feed

import logging

import urllib

#
# Import Local modules
#
from oneoffcast import models
from oneoffcast.util import *

#
# Module
#

class UserFeed(Feed):

    title_template = 'feed_title.html'
    description_template = 'feed_description.html'

    def get_object(self, bits):
        return User.objects.get(username=bits[0])
    
    def title(self, obj):
        return "%s's CastSampler Feed" % obj.username
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def description(self, obj):
        return 'CastSampler feed assembled for %s' % obj.username

    def item_link(self, obj):
        return obj.link
    
    def item_enclosure_url(self, obj):
        return obj.item_enclosure_url
    
    def item_enclosure_length(self, obj):
        return obj.item_enclosure_length
    
    def item_enclosure_mime_type(self, obj):
        return obj.item_enclosure_mime_type

    def item_author_name(self, obj):
        return obj.author_name

    def item_author_email(self, obj):
        return obj.author_email

    def item_pubdate(self, obj):
        return obj.add_date

    def items(self, obj):
        return models.QueueItem.objects.filter(user=obj).order_by('add_date')

class UniqueGUIDRSSFeed(Rss201rev2Feed):

    _existing_unique_ids = set()

    def add_item(self, link=None, unique_id=None, enclosure=None, **kwds):
        #
        # Switch the unique_id if it refers to the link because
        # some sites (Barnes and Noble) use the same link for all
        # enclosures but the enclosure url is still different.
        #
        if (link == unique_id) and (enclosure is not None):
            unique_id = enclosure.url
        return Rss201rev2Feed.add_item(self,
                                       link=link,
                                       unique_id=unique_id,
                                       enclosure=enclosure,
                                       **kwds)

class RSSFeed(UserFeed):
    feed_type = UniqueGUIDRSSFeed






class ProxyFeedArgs:
    "Container for ProxyFeed arguments"

    def __init__(self, username, podcastid):
        self.user = User.objects.get(username=username)
        self.podcast = models.Podcast.objects.get(id=podcastid)
        return

    def get_absolute_url(self):
        return 

class ProxyFeed(Feed):
    """This feed uses item links which add the episode to the user's queue
    instead of linking to the real site.
    """
    feed_type = UniqueGUIDRSSFeed

    title_template = 'monitor_title.html'
    description_template = 'monitor_description.html'

    def __init__(self, slug, feed_url):
        Feed.__init__(self, slug, feed_url)
        self.current_site = Site.objects.get_current()
        return

    def get_object(self, bits):
        try:
            self.__args = ProxyFeedArgs(bits[0], bits[1])
        except IndexError:
            raise ValueError('Invalid URL.  Specify username/podcastid')
        return self.__args
    
    def title(self, obj):
        return 'CastSampler Monitor Feed: %s' % obj.podcast.name
    
    def link(self, obj):
        # FIXME - Should point to a view of the feed on CastSampler site
        return obj.podcast.home_url

    def items(self, obj):
        logging.debug('Fetching podcast contents...')
        parsed_feed = obj.podcast.get_current_feed_contents()
        logging.debug('Found %d entries' % len(parsed_feed['entries']))
        for entry in parsed_feed['entries']:
            entry.podcast = self.__args.podcast
        return parsed_feed['entries']
    
    def item_link(self, entry):
        """Replace the real link to the item with one to add
        the item to the user's queue.
        """
        logging.debug('ProxyFeed.item_link(%s)' % entry)

        url_args = { 'podcast':self.__args.podcast.id,
                     'title':entry['title'].encode('UTF-8'),
                     'summary':entry['summary'].encode('UTF-8'),
                     }

        try:
            enclosure = entry['enclosures'][0]
        except (KeyError, IndexError):
            enclosure = None
            
        author_detail = entry.get('author_detail')
        if author_detail:
            url_args['author_name'] = author_detail['name'].encode('UTF-8')
            url_args['author_email'] = author_detail['email'].encode('UTF-8')
        else:
            author_name = entry['author']
            url_args['author_name'] = author_name
            if author_name:
                url_args['author_email'] = 'n/a'
            else:
                url_args['author_name'] = ''
                url_args['author_email'] = ''

        if entry['link']:
            url_args['link'] = entry['link'].encode('UTF-8')
        elif enclosure:
            url_args['link'] = enclosure['href'].encode('UTF-8')
        else:
            url_args['link'] = ''
        
        if enclosure:
            url_args['item_enclosure_url'] = enclosure['href'].encode('UTF-8')
            url_args['item_enclosure_mime_type'] = enclosure['type'].encode('UTF-8')
            url_args['item_enclosure_length'] = enclosure['length'].encode('UTF-8')

        logging.debug('url_args = %s' % str(url_args))
        encoded_args = urllib.urlencode(url_args)
        logging.debug('encoded_args = %s' % encoded_args.encode('UTF-8'))

        return ('/cast/%s/add_to_queue?' % self.__args.user.username) + encoded_args
