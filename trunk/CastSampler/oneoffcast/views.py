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
from django.contrib.auth import LOGIN_URL, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import serializers
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, Context

import feedfinder

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

    #
    # Look up some data we need for the page
    #
    subscriptions = [ sub.as_dict(request.user)
                      for sub in request.user.podcast_set.filter(allowed=True).order_by('name')
                      ]
    json_subscriptions = simplejson.dumps(subscriptions)
    queue = [ qi.as_dict()
              for qi in QueueItem.objects.filter(user=request.user).order_by('-add_date')
              ]
    json_queue = simplejson.dumps(queue)
        
    return render_to_response('user.html',
                              {'user':request.user,
                               'add_feed':add_feed_form,
                               'subscriptions':json_subscriptions,
                               'queue':json_queue,
                               })


def subscriptions(request, username=None, feed_id=None):
    """Do something with the user's subscription list.
    """
    logging.debug('subscriptions %s' % request.method)

    if request.method == 'GET':
        #
        # Provide an OPML file with the list of feeds
        #
        subscriptions = request.user.podcast_set.filter(allowed=True).order_by('name')

        #
        # Really, there isn't an easier way to set the mimetype without having
        # to render the entire template ourselves?
        #
        response = HttpResponse(mimetype='text/x-opml')
        response['Content-Disposition'] = 'attachment; filename=castsampler.opml'
        t = loader.get_template('subscriptions.opml')
        c = Context({'user':request.user,
                     'subscriptions':subscriptions,
                     'url_prefix':'http://' + Site.objects.get_current().domain,
                     })
        response.write(t.render(c))
        return response
    #
    # If they used another request method, they must be trying
    # to modify the list of subscriptions.
    #
    return change_subscriptions(request, username=username, feed_id=feed_id)

@jsonView()
@same_user_only()
@login_required
def change_subscriptions(request, username=None, feed_id=None):
    """Modify the user's subscription list.
    """
    response = {}
    logging.debug('change_subscriptions %s' % request.method)
    
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

        #
        # If the URL does not look like a feed, see if we
        # can find a single feed from the URL.
        #
        url = new_data['url']
        logging.debug('Checking %s for a feed' % url)
        feed_guesses = feedfinder.feeds(url)
        logging.debug('Found %s feed urls' % str(feed_guesses))
        if url not in feed_guesses:
            if feed_guesses:
                new_data['url'] = feed_guesses[0]
                logging.debug('Using %s instead' % new_data['url'])

        #
        # We are ready to save the feed info to the database
        #
        podcast, parsed_feed = manipulator.save(new_data)

        response.update(podcast.as_dict(request.user))
        response['entries'] = convert_feed_to_entries(parsed_feed)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('%s?%s=%s' % (LOGIN_URL, REDIRECT_FIELD_NAME, quote(request.get_full_path())))
        if request.user.username != username:
            raise RuntimeError('You are not allowed to remove subscriptions for another user.')

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

def _do_add_to_queue(user, data):
    "Really do the work to add an item to the user's queue."

    # Process the form input and check for errors
    new_data = data.copy()
    new_data['user'] = user.id

    logging.debug('_do_add_to_queue(%s)' % str(data))

    # Fix up the length in case it is invalid
    length = new_data.get('item_enclosure_length', 0)
    try:
        length = int(length)
    except (TypeError, ValueError):
        length = 0
    new_data['item_enclosure_length'] = length

    manipulator = QueueItem.AddManipulator()
    manipulator.do_html2python(new_data)
    new_item = manipulator.save(new_data)
    return new_item


@jsonView()
@same_user_only()
@login_required
def queue(request, username):
    """Returns JSON package of current queue contents for the user.
    """
    logging.debug('queue(%s) %s' % (username, request.method))

    response = {}
    
    if request.method == 'POST':
        new_item = _do_add_to_queue(request.user, request.POST)
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


@same_user_only()
@login_required
def add_to_queue(request, username):
    logging.debug('add_to_queue(%s)' % username)
    logging.debug(str(request.GET))
    
    # Add the new item
    _do_add_to_queue(request.user, request.GET)

    # Redirect to the user page
    return user_redirect(request)


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
    response['name'] = podcast.name
    return response
