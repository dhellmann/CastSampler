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
from django import template

#
# Import Local modules
#
from oneoffcast.models import Podcast

#
# Module
#

register = template.Library()

@register.inclusion_tag('newest_subscription_list.html')
def newest_subscription_list(count=5):
    """Show a list of the most recently added subscriptions.
    """
    count = int(count)
    newest_subscriptions = Podcast.objects.all().order_by('-registration_date')[:count]
    return {'newest_subscriptions':newest_subscriptions,
            }

@register.inclusion_tag('popular_subscription_list.html')
def popular_subscription_list(count=5):
    """Show a list of the popular subscriptions based on individual show subscription count.
    """
    count = int(count)

    #
    # Look for how many individual episodes from a given subscription are referenced.
    # Do we want to change this to count references to a subscription by a user
    # instead of individual episodes?
    #
    popular_subscriptions_query = Podcast.objects.extra(
        select={'use_count':"""select count(*)
                               from oneoffcast_queueitem
                               where oneoffcast_queueitem.podcast_id = oneoffcast_podcast.id
                               """,
                },
        ).order_by('-use_count')
    popular_subscriptions = []
    for p in popular_subscriptions_query:
        if p.use_count <= 0:
            break
        popular_subscriptions.append(p)
        if len(popular_subscriptions) >= count:
            break

    return { 'popular_subscriptions':popular_subscriptions }
