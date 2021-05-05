"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth, T
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'bird',
    ### TODO: define the fields that are in the json.
    Field('bird', requires=IS_NOT_EMPTY()),
    Field('weight', 'integer', default=0, requires=IS_INT_IN_RANGE(0, 1e6)),
    Field('diet', 'string', requires=IS_NOT_EMPTY()),
    Field('habitat', 'string', requires=IS_NOT_EMPTY()),
    Field('n_sightings', 'integer', default=1, requires=IS_INT_IN_RANGE(1, 1e6)),
    Field('user_email', default=get_user_email)
)

db.bird.id.readable = db.bird.id.writable = False
db.bird.user_email.readable = db.bird.user_email.writable = False

db.bird.bird.label = T('Bird')
db.bird.weight.label = T('Weight')
db.bird.diet.label = T('Diet')
db.bird.habitat.label = T('Habitat')
db.bird.n_sightings.label = T('Bird Count')
db.bird.user_email.label = T('User Email')

db.commit()
