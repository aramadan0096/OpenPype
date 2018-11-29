import os
import sys
import re
import ftrack_api
from ftrack_event_handler import BaseEvent
from app import api

class Test_Event(BaseEvent):

    def launch(self, session, entities, event):

        '''just a testing event'''
        exceptions = ['assetversion', 'job', 'user', 'reviewsessionobject', 'timer', 'socialfeed', 'timelog']
        self.show_message(event,"Test",True)
        self.log.info(event['source'])
        return True


def register(session, **kw):
    '''Register plugin. Called when used as an plugin.'''
    if not isinstance(session, ftrack_api.session.Session):
        return

    event = Test_Event(session)
    event.register()
