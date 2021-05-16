"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def get_user():
    return auth.current_user.get('id') if auth.current_user else None


### Define your table below
#
db.define_table('post', Field('posts'))
db.define_table('thumb',
                Field('post', 'reference posts'),
                Field('thumbup', 'integer', default=0),
                Field('thumbdown', 'integer', default=0),
                Field('rater', 'reference auth_user', default=get_user)
                )
#
## always commit your models to avoid problems later

db.commit()
