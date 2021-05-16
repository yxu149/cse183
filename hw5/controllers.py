"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email, get_user

url_signer = URLSigner(session)



@action('index')
@action.uses(db, auth, 'index.html')
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
        load_post_url = URL('load_post', signer=url_signer),
        add_post_url = URL('add_post', signer=url_signer),
        delete_post_url = URL('delete_post', signer=url_signer),
        get_like_url = URL('get_rating', signer=url_signer),
        set_rating_url = URL('set_rating', signer=url_signer),


    )

@action('load_post')
@action.uses(url_signer.verify(), db)
def load_post():
    rows = db(db.post).select().as_list()
    return dict(rows=rows)

@action('add_post', method="POST")
@action.uses(url_signer.verify(), db)
def add_post():
    id = db.post.insert(
        posts=request.json.get('post'),
    )
    return dict(id=id)

@action('delete_post')
@action.uses(url_signer.verify(), db)
def delete_post():
    id = request.params.get('id')
    assert id is not None
    db(db.post.id == id).delete()
    return "ok"

@action('get_rating')
@action.uses(url_signer.verify(), db, auth.user)
def get_rating():
    """Returns the rating for a user and an image."""
    id = request.params.get('id')
    row = db((db.thumb.post == id) &
             (db.thumb.rater == get_user())).select().first()
    rating = row.rating if row is not None else 0
    return dict(rating=rating)


@action('set_rating', method='POST')
@action.uses(url_signer.verify(), db, auth.user)
def set_rating():
    """Sets the rating for an image."""
    id = request.json.get('id')
    rating = request.json.get('rating')
    assert id is not None and rating is not None
    db.post.update_or_insert(
        ((db.thumb.post == id) & (db.thumb.rater == get_user())),
        post=id,
        rater=get_user(),
        rating=rating
    )
    return "ok"