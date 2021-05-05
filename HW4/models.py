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


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'contact',
    Field('first_Name', requires=IS_NOT_EMPTY()),
    Field('last_Name', requires=IS_NOT_EMPTY()),
    Field('user_Email', default=get_user_email)
)

db.define_table(
    'phone',
    Field('contact_id', 'reference contact'),
    Field('phone_Number'),
    Field('phone_Name')
)

db.contact.id.readable = db.contact.id.writable = False
db.contact.user_Email.readable = db.contact.user_Email.writable = False
db.phone.contact_id.readable = db.phone.contact_id.writable = False


db.commit()
