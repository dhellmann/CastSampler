#
# Copyright (c) 2006 Racemi, Inc.  All rights reserved.
#

"""Various form manipulators

"""

_module_id_ = '$Id$'

#
# Import system modules
#
from django import forms


#
# Import Local modules
#


#
# Module
#

class ShowFeedContentsForm(forms.Manipulator):
    """Define the elements of the form we use to
    show the contents of a feed (user submits URL).
    """

    def __init__(self):
        self.fields = (
            forms.URLField(field_name='url',
                           is_required=True,
                           ),
            )
        return

    def save(self, new_data):
        raise NotImplementedError('Do not know how to save a ShowFeedContentsForm yet')
    
