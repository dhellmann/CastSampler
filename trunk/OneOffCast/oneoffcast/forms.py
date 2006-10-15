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

"""Various form manipulators

"""

#
# Import system modules
#
from django import forms

#
# Import Local modules
#
from oneoffcast.models import find_or_create_podcast

#
# Module
#

class AddFeedForm(forms.Manipulator):
    """Define the elements of the form we use to
    show the contents of a feed (user submits URL).
    """

    def __init__(self, user=None):
        self.user = user
        self.fields = (
            forms.URLField(field_name='url',
                           is_required=True,
                           ),
            )
        return

    def save(self, new_data):
        url = new_data['url']
        return find_or_create_podcast(url, user=self.user)
