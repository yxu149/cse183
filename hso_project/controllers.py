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
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash, Field
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma
from pydal.validators import *


url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth.user, 'index.html')
def index():
    #print("User:", get_user_email())
    rows=db(db.contact.user_Email == get_user_email()).select().as_list()
    print(rows)
    for row in rows:
        #print(row)
        row["phone_Numbers"]=""
        s = db(db.phone.contact_id == row['id']).select()
        #print(s)
        for r in s:
            #print(r)
            if(row["phone_Numbers"] != ""):
                row["phone_Numbers"]=row["phone_Numbers"]+" , "
            row["phone_Numbers"]=row["phone_Numbers"]+r['phone_Number']+" ("+r['phone_Name']+") "
    return dict(rows = rows, url_signer=url_signer)

@action('add', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add.html')
def add():
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if(form.accepted):
        redirect(URL('index'))
    return dict(form=form)

@action('edit/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify(), 'edit.html')
def edit(contact_id = None):
    #check the contact_id is not None, if it is not None, continues. Otherwise, return error message
    assert contact_id is not None
    #first()  method use the information from the database.
    #to obtain the information of contact_id row.
    p=db(db.contact.id == contact_id).select().first()
    if p is None:
        redirect(URL('index'))
    form=Form(db.contact, csrf_session=session, record=p ,deletable=False, formstyle=FormStyleBulma)
    if(form.accepted):
        redirect(URL('index'))
    return dict(form=form)

@action('delete/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify())
def delete(contact_id=None):
    assert contact_id is not None
    #delete() method delete the contact_id row
    db(db.contact.id == contact_id).delete()
    redirect(URL('index'))

@action('edit_phones/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify(), 'edit_phones.html')
def edit_phones(contact_id=None):
    assert contact_id is not None
    # only can show the information of contact_id in phone page
    rows=db(
        (db.contact.id == contact_id) &
        (db.phone.contact_id == contact_id) &
        (db.phone.contact_id == db.contact.id)
    ).select()

    #choose the database that belong to user_email and send the name to phone page
    names=db(
        (db.contact.user_Email == get_user_email()) &
        (db.contact.id == contact_id) 
    ).select().first()
    #print(rows)
    assert rows is not None
    name=names.first_Name+" "+names.last_Name
    return dict(name=name, rows=rows, url_signer=url_signer, contact_id=contact_id)

@action('add_phone/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify(), 'add_phone.html')
def add_phone(contact_id=None):
    assert contact_id is not None
    #choose the database that belong to user_email and send the name to add_phone page
    phones=db(
            (db.contact.user_Email == get_user_email()) &
            (db.contact.id == contact_id) 
    ).select().first()
    assert phones is not None
    #print(phones)
    # get the owner of phone
    name=phones.first_Name+" "+phones.last_Name
    form=Form([Field('phone',requires=IS_NOT_EMPTY()), Field('kind', requires=IS_NOT_EMPTY())], csrf_session=session, formstyle=FormStyleBulma)
    if(form.accepted):
        #insert the form
        db.phone.insert(
            contact_id=contact_id,
            phone_Number=form.vars['phone'],
            phone_Name=form.vars['kind']
        )
        redirect(URL('edit_phones', contact_id, signer=url_signer))
    return dict(name=name, form=form)


@action('edit_phone/<contact_id:int>/<phone_id:int>', method=['GET', 'POST'])
@action.uses(db, session, auth.user, url_signer.verify(), 'edit_phone.html')
def edit_phone(contact_id=None, phone_id=None):
    assert contact_id is not None
    assert phone_id is not None
    p=db(
        (db.phone.id == phone_id) &
        (db.phone.contact_id == contact_id) &
        (db.phone.contact_id == db.contact.id)
    ).select().first()
    assert p is not None
    #print(p)
    name=p.contact.first_Name+" "+p.contact.last_Name
    form=Form([Field('phone'), Field('kind')],
        record=dict(phone=p.phone.phone_Number, kind=p.phone.phone_Name),
        deletable=False,
        csrf_session=session,
        formstyle=FormStyleBulma
    )
    if(form.accepted):
        #To use update() method for the dictionary, we need use db(db[tablename].id == id).update()
        db(db['phone'].id == phone_id).update(
            phone_Number=form.vars['phone'],
            phone_Name=form.vars['kind']
        )
        redirect(URL('edit_phones', contact_id, signer=url_signer))
    return dict(form=form, name=name)

@action('delete_phone/<contact_id:int>/<phone_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify())
def delete_phone(contact_id=None, phone_id=None):
    assert contact_id is not None
    assert phone_id is not None
    db(
        (db.phone.id == phone_id) &
        (db.phone.contact_id == contact_id)
    ).delete()
    redirect(URL('edit_phones', contact_id, signer=url_signer))
