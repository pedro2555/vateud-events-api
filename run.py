# -*- coding: utf-8 -*-

"""
    Eve Demo
    ~~~~~~~~

    A demostration of a simple API powered by Eve REST API.

    The live demo is available at eve-demo.herokuapp.com. Please keep in mind
    that the it is running on Heroku's free tier using a free MongoHQ
    sandbox, which means that the first request to the service will probably
    be slow. The database gets a reset every now and then.

    :copyright: (c) 2016 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os
from eve import Eve

import requests
import json

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    host = '0.0.0.0'
else:
    port = 5000
    host = '127.0.0.1'

app = Eve()

def pre_events_get_callback(request, lookup):
    # load events from the server
    r = requests.get('http://api.vateud.net/events.json')

    # early exit on non 200 responses, we're not expecting anything else
    if r.status_code != 200:
        return

    events_collection = app.data.driver.db['events']
    events = json.loads(r.text)
    for event in events:
        # early exit on existing events (not sure if they update the things or
        # not, but theres no etag, or any other evident versioning scheme, so
        # we're skiping on updated records until that is clarified)
        if events_collection.find_one({'vateud_id': event['id']}):
            continue

        events_collection.insert_one({
            'vateud_id': event['id'],
            'title': event['title'],
            'subtitle': event['subtitle'],
            'description': event['description'],
            'airports': event['airports'].split(', '),
            'banner_url': event['banner_url'],
            'starts': event['starts'],
            'ends': event['ends']
        })

app.on_pre_GET_events += pre_events_get_callback

if __name__ == '__main__':
    app.run(host=host, port=port)
