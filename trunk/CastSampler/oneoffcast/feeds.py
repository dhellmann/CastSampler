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
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed


#
# Import Local modules
#
from oneoffcast import models


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
        return models.QueueItem.objects.filter(user=obj).order_by('-add_date')

class RSSFeed(UserFeed):
    feed_type = Rss201rev2Feed

class AtomFeed(UserFeed):
    feed_type = Atom1Feed
