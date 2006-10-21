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

"""OneOffCast app views

"""

#
# Import system modules
#
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

import logging

#
# Import Local modules
#
from oneoffcast.models import Podcast, QueueItem
from oneoffcast.forms import AddFeedForm
from oneoffcast.util import *

#
# Module
#

def main(request):
    """Main page for the app.
    """
    #
    # The 10 most recently added podcasts.
    #
    newest_podcasts = Podcast.objects.all().order_by('-registration_date')[:10]
    #
    # Look for how many individual episodes from a given podcast are referenced.
    # Do we want to change this to count references to a podcast by a user
    # instead of individual episodes?
    #
    popular_podcasts = Podcast.objects.extra(
        select={'use_count':"""select count(*)
                               from oneoffcast_queueitem
                               where oneoffcast_queueitem.podcast_id = oneoffcast_podcast.id
                               """,
                },
        where=['use_count > 0'], # only include podcasts referenced by *someone*
        ).order_by('-use_count')[:10]
    return render_to_response('index.html', 
                              {'newest_podcasts':newest_podcasts,
                               'popular_podcasts':popular_podcasts,
                               'user':request.user,
                               })

@login_required
def user_redirect(request, urlBase='/cast'):
    """Redirect the user to their user page.
    """
    return HttpResponseRedirect('%s/%s' % (urlBase, request.user.username))


@login_required
@same_user_only()
def user(request, username):
    """Show information about the user.
    """
    #
    # Build up a form for adding by the feed
    #
    if request.POST:
        manipulator = AddFeedForm()
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        add_feed_form = forms.FormWrapper(manipulator, new_data, errors)
    else:
        add_feed_form = AddFeedForm()
    
    return render_to_response('user.html',
                              {'user':request.user,
                               'add_feed':add_feed_form,
                               })



@jsonView()
@login_required
@same_user_only()
def add_feed(request, username=None):
    """The user wants to add items from a feed they are giving us.
    """
    response = {}
    
    if request.POST:
        #
        # Process the form input and check for errors
        #
        manipulator = AddFeedForm(request.user)
        new_data = request.POST.copy()

        errors = manipulator.get_validation_errors(new_data)
        if errors:
            error_text = ', '.join([str(e) for e in errors.get('url', [])])
            raise RuntimeError(error_text)
            
        manipulator.do_html2python(new_data)
        podcast, parsed_feed = manipulator.save(new_data)
        
        response['podcast_name'] = podcast.name
        response['podcast_id'] = podcast.id

    return response

@jsonView()
@same_user_only()
@login_required
def queue(request, username):
    """Returns JSON package of current queue contents for the user.
    """
    logging.debug('looking for queue for %s' % username)
    #
    # The items already in their queue
    #
    queued_items = QueueItem.objects.filter(user=request.user).order_by('add_date')
    response = { 'queue': [ { 'podcast_name':qi.podcast.name,
                              'podcast_home':qi.podcast.home_url,
                              'title':qi.title,
                              'link':qi.link,
                              'description':qi.get_truncated_description(),
                              'enclosure_url':qi.item_enclosure_url,
                              'enclosure_mimetype':qi.item_enclosure_mime_type,
                              #'pubdate':qi.add_date,
                              }
                            for qi in queued_items
                            ],
                 }
    return response

