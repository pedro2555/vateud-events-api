# -*- coding: utf-8 -*-

"""
    eve-demo settings
    ~~~~~~~~~~~~~~~~~

    Settings file for our little demo.

    PLEASE NOTE: We don't need to create the two collections in MongoDB.
    Actually, we don't even need to create the database: GET requests on an
    empty/non-existant DB will be served correctly ('200' OK with an empty
    collection); DELETE/PATCH will receive appropriate responses ('404' Not
    Found), and POST requests will create database and collections when needed.
    Keep in mind however that such an auto-managed database will most likely
    perform poorly since it lacks any sort of optimized index.

    :copyright: (c) 2016 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os

# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', '')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'vateud-events')

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

X_DOMAINS = ('http://127.0.0.1:8081', 'https://vateud-events.herokuapp.com')
X_HEADERS = ('content-type', 'if-match')

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

events = {
    'item_title': 'event',
    'schema': {
        # this is just used for definitely avoid duplicated records
        # and quite a nice way to keep track of things overall
        'vateud_id': {
            'type': 'integer',
            'unique': True
        },
        'title': {
            'type': 'string'
        },
        'subtitle': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'airports': {
            'type': 'list'
        },
        'banner_url': {
            'type': 'string'
        },
        'starts': {
            'type': 'datetime'
        },
        'ends': {
            'type': 'datetime'
        }
    }
}

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'events': events
}
