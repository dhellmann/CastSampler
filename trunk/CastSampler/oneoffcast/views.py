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
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson

import logging

#
# Import Local modules
#
from oneoffcast.models import Podcast, QueueItem
from oneoffcast.forms import AddFeedForm


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
def user(request, username):
    """Show information about the user.
    """
    if request.user.username != username:
        raise RuntimeError('You are not allowed to see this page')

    #
    # The items already in their queue
    #
    queued_items = QueueItem.objects.filter(user=request.user).order_by('add_date')

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
                              {'queued_items':queued_items,
                               'user':request.user,
                               'add_feed':add_feed_form,
                               })


def ajaxErrorHandling():
    """Simple decorator to log and return error messages.
    """
    def decorator(func):

        def newfunc(self, *args, **kw):
            try:
                output = func(self, *args, **kw)
            except Exception, err:
                logging.exception(err)
                return HttpResponse('<div class="error">%s</div>' % err)
            return output
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator

def jsonView():
    """Simple decorator to convert the response to a json message.
    """
    def decorator(func):

        def newfunc(self, *args, **kw):
            try:
                output = func(self, *args, **kw)
                if not 'error' in output:
                    output['error'] = None
            except Exception, err:
                logging.exception(err)
                output = { 'error':str(err) }

            json_response = simplejson.dumps(output)
            return HttpResponse(json_response)
        
        newfunc.func_name = func.func_name
        newfunc.exposed = True
        return newfunc

    return decorator


@jsonView()
def add_feed(request, username=None):
    """The user wants to add items from a feed they are giving us.
    """
    logging.debug('calling add_feed')
    if request.user.username != username:
        raise RuntimeError('You are not allowed to see this page')

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
    