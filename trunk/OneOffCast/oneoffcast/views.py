#
# $Id$
#

"""OneOffCast app views
"""

from django.http import HttpResponse
from django.shortcuts import render_to_response

from oneoffcast.models import Podcast

def main(*args, **nargs):
    """Main page for the app.
    """
    newest_podcasts = Podcast.objects.all().order_by('-registration_date')[:10]
    return render_to_response('oneoffcast/index.html', 
                              {'newest_podcasts':newest_podcasts,
                               })


