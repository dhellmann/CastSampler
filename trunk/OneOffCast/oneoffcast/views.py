#
# $Id$
#

"""OneOffCast app views
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from django.contrib.auth.models import User	

from oneoffcast.models import Podcast, QueueItem

def main(request):
    """Main page for the app.
    """
    newest_podcasts = Podcast.objects.all().order_by('-registration_date')[:10]
    popular_podcasts = Podcast.objects.all()[:10]
    return render_to_response('oneoffcast/index.html', 
                              {'newest_podcasts':newest_podcasts,
                               'popular_podcasts':popular_podcasts,
                               })


@login_required
def user(request, username):
    """Show information about the user.
    """
    if request.user.username == username:
        queued_items = QueueItem.objects.filter(user=request.user).order_by('-add_date')
        return render_to_response('oneoffcast/user.html',
                                  {'queued_items':queued_items,
                                   })
    else:
        raise RuntimeError('You are not allowed to see this page')