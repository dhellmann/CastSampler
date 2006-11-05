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
    newest_podcasts = Podcast.objects.all().order_by('-registration_date')[:5]
    #
    # Look for how many individual episodes from a given podcast are referenced.
    # Do we want to change this to count references to a podcast by a user
    # instead of individual episodes?
    #
    popular_podcasts_query = Podcast.objects.extra(
        select={'use_count':"""select count(*)
                               from oneoffcast_queueitem
                               where oneoffcast_queueitem.podcast_id = oneoffcast_podcast.id
                               """,
                },
        ).order_by('-use_count')
    popular_podcasts = []
    for p in popular_podcasts_query:
        if p.use_count <= 0:
            break
        popular_podcasts.append(p)
        if len(popular_podcasts) >= 5:
            break
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
    new_data = {}
    if request.POST:
        new_data = request.POST.copy()
    elif request.GET:
        new_data = request.GET.copy()

    if new_data:
        manipulator = AddFeedForm()
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
def subscriptions(request, username=None, feed_id=None):
    """Do something with the user's subscription.
    """
    logging.debug('subscriptions %s' % request.method)
    response = {}
    
    if request.method == 'POST':
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

        response.update(podcast.as_dict())
        response['entries'] = convert_feed_to_entries(parsed_feed)

    elif request.method == 'DELETE':
        logging.debug('Deleting %s' % feed_id)

        #
        # Remove the podcast from the user's subscriptions
        #
        podcast = Podcast.objects.get(id=feed_id)
        podcast.users.remove(request.user)
        response['removed'] = feed_id

        #
        # Remove any queue items from that podcast from
        # the user's queue.
        #
        for item in QueueItem.objects.filter(user=request.user,
                                             podcast=podcast,
                                             ):
            item.delete()

    return response


@jsonView()
@same_user_only()
@login_required
def queue(request, username):
    """Returns JSON package of current queue contents for the user.
    """
    logging.debug('queue(%s) %s' % (username, request.method))

    response = {}
    
    if request.method == 'POST':
        #
        # Process the form input and check for errors
        #
        new_data = request.POST.copy()
        new_data['user'] = request.user.id

        #
        # Fix up the length in case it is invalid
        #
        length = new_data.get('item_enclosure_length', 0)
        try:
            length = int(length)
        except (TypeError, ValueError):
            length = 0
        new_data['item_enclosure_length'] = length

        manipulator = QueueItem.AddManipulator()
        manipulator.do_html2python(new_data)
        new_item = manipulator.save(new_data)

        response['add_to_queue'] = [ new_item.as_dict() ]
        
    elif request.method == 'GET':
        #
        # The items already in their queue
        #
        queued_items = QueueItem.objects.filter(user=request.user).order_by('-add_date')
        response['queue'] = [ qi.as_dict()
                              for qi in queued_items
                              ]
    #logging.debug(response)
    return response

@jsonView()
@same_user_only()
@login_required
def remove_from_queue(request, username, id):
    """Remove id from the queue.
    """
    logging.debug('remove_from_queue(%s, %s) %s' % (username, id, request.method))

    removed = []
    response = {'remove_from_queue':removed,
                }
    
    if request.method == 'DELETE':
        item = QueueItem.objects.get(id=id)
        item.delete()
        removed.append(id)

    #logging.debug(response)
    return response


@jsonView()
@same_user_only()
@login_required
def feed_list(request, username):
    """Returns JSON package of podcasts for the user.
    """
    l = []
    response = { 'list': l }
    for p in request.user.podcast_set.filter(allowed=True).order_by('name'):
        l.append(p.as_dict())
    return response

@jsonView()
@login_required
def external(request, id):
    """Returns JSON package of podcast entries for the
    specified podcast.
    """
    logging.debug('looking for %s' % id)
    podcast = Podcast.objects.get(id=id)
    parsed_feed = podcast.get_current_feed_contents()
    response = {}
    response['entries'] = convert_feed_to_entries(parsed_feed)
    response['id'] = id
    return response
