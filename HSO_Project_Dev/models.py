"""
This file defines the database models
"""

import datetime
import uuid
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_uuid():
    return uuid.uuid4()
### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

#-------------------user table-----------------------
db.define_table(
    'user',
    Field('first_name', requires=IS_NOT_EMPTY()),
    Field('last_name', requires=IS_NOT_EMPTY()),
    Field('uuid', requires=IS_NOT_EMPTY()),
    Field('email', requires=IS_NOT_EMPTY()),
)
#====================================================


#-------------------user_option_Infomation table------------------------------------------------
db.define_table(
    'user_option_Info',
    Field('user_id', 'reference user'),
    Field('user_image', 'text'),
    Field('nickname'),
    Field('sex'),
    Field('day'),
    Field('month'),
    Field('year'),
    Field('age'),
    Field('zip_code'),
    Field('user_description', 'text', default="Sorry, I do not write anything right now ^_^!")
)

db.user_option_Info.user_id.readable = db.user_option_Info.user_id.writable = False
#================================================================================================


#-------------------product table------------------------------------------------
db.define_table(
    'product',
    Field('user_id', 'reference user'),
    Field('product_name'),
    Field('quantity', 'integer'),
    Field('price', 'float'),
    Field('image', 'text'), # Data URL for the image.
    Field('description', 'text', default="Sorry, the owner do not add any description!"),
)

db.product.id.readable = db.product.id.writable = False
db.product.user_id.readable = db.product.user_id.writable = False

db.define_table(
    'more_image',
    Field('product_id', 'reference product'),
    Field('more_image', 'text'),
)

db.define_table(
    'product_post',
    Field('product_id', 'reference product'),
    Field('user_id', 'reference user'),
    Field('post_content'),
    Field('post_username'),
    Field('post_user_image', 'text'),
)
#================================================================================================


#-------------------user_rate_it table------------------------------------------------
db.define_table(
    'user_rate_it',
    Field('user_rate'),
    Field('user_role'),
    Field('rater_id'),
    Field('rater_email')
)
#================================================================================================

#-------------------Community post and reply table------------------------------------------------
db.define_table(
    'post',
    Field('user_id', 'reference user'),
    Field('post_content'),
    Field('post_username'),
    Field('post_user_image', 'text'),
)

db.define_table(
    'thumbs',
    Field('post_id', 'reference post'),
    Field('rating_up', 'boolean', default=None),
    Field('rating_down', 'boolean', default=None),
    Field('rater', 'reference auth_user', default=get_user)
)

db.define_table(
    'rater_person',
    Field('rate_id','reference thumbs'),
    Field('first_Name'),
    Field('last_Name')
)

#================================================================================================

#--------------------------Wishlist---------------------------------------
db.define_table(
    'wishlist',
    Field('user_id', 'reference user'),
    Field('product_id', 'reference product'),
    Field('product_owner'),
    Field('product_name'),
    Field('quantity', 'integer'),
    Field('price', 'float'),
    Field('image', 'text'), # Data URL for the image.
    Field('description', 'text', default="Sorry, the owner do not add any description!"),
)

db.product.id.readable = db.product.id.writable = False
db.product.user_id.readable = db.product.user_id.writable = False



db.commit()
