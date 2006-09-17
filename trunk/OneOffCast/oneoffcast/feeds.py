#
# $Id$
#
"""Feed generation
"""

from django.contrib.auth.models import User
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from oneoffcast import models

class UserFeed(Feed):
    feed_type = Atom1Feed

    def get_object(self, bits):
        return User.objects.get(username=bits[0])
    
    def title(self, obj):
        return '%s OneOffCast' % obj.username
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def description(self, obj):
        return 'OneOffCast assembled for %s' % obj.username
    
    def item_enclosure_url(self, obj):
        return obj.item_enclosure_url
    
    def item_enclosure_length(self, obj):
        return obj.item_enclosure_length
    
    def item_enclosure_mime_type(self, obj):
        return obj.item_enclosure_mime_type

    def items(self, obj):
        return models.QueueItem.objects.filter(user=obj).order_by('-add_date')