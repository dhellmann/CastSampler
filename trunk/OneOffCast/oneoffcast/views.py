#
# $Id$
#

"""OneOffCast app views
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from django.contrib.auth.models import User	

from oneoffcast.models import Podcast, QueueItem

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
    return render_to_response('oneoffcast/index.html', 
                              {'newest_podcasts':newest_podcasts,
                               'popular_podcasts':popular_podcasts,
                               'user':request.user,
                               })

@login_required
def login_redirect(request):
    """Redirect the user to their user page.
    """
    return HttpResponseRedirect('/cast/%s' % request.user.username)

@login_required
def user(request, username):
    """Show information about the user.
    """
    if request.user.username == username:
        queued_items = QueueItem.objects.filter(user=request.user).order_by('-add_date')
        return render_to_response('oneoffcast/user.html',
                                  {'queued_items':queued_items,
                                   'user':request.user,
                                   })
    else:
        raise RuntimeError('You are not allowed to see this page')