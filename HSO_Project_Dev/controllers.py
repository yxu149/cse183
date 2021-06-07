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
from .models import get_user_email, get_uuid, get_user
from py4web.utils.form import Form, FormStyleBulma
from pydal.validators import *
import uuid
import random

#TODO: 需删除以下部分
EXAMPLE_USER = "qhuang24@ucsc.edu"

url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth, 'index.html')
def index():
    #加入本地的user database中
    if get_user_email() is not None:
        check_user=db(db.user.email == get_user_email()).select().first()
        if check_user == None:
            userInfo=db(db.auth_user.email == get_user_email()).select().first()
            db.user.insert(
                first_name=userInfo.first_name,
                last_name=userInfo.last_name,
                uuid=get_uuid(),
                email=userInfo.email
            )
    #TODO: 修改选择商品通过判断它的星星数量进行推荐
    return dict(
        searchBar_url = URL('searchBar', signer=url_signer),
        get_username_url = URL('get_username', signer=url_signer),
        get_products_url = URL('get_products', signer=url_signer),
        add_wishlist_url = URL('add_wishlist', signer=url_signer),
    )

@action('get_username')
@action.uses(db, url_signer.verify())
def get_username():
    #TODO: 修改EXAMPLE_USER为get_user_email（）去主动获得当前用户信息
    if get_user_email() is not None:
        userInfo=db(db.user.email == get_user_email()).select().first()
        userInfo_N=db(db.user_option_Info.user_id == userInfo.id).select().first()
        if userInfo_N != None:
            if userInfo_N.nickname != None:
                userName=userInfo_N.nickname
            else:
                userName=userInfo.first_name +" "+userInfo.last_name
        else:
            userName=userInfo.first_name +" "+userInfo.last_name
    else:
        userName = ""
    return dict(userName=userName)

@action('get_products')
@action.uses(db, url_signer.verify())
def get_products():
    products=db(db.product).select().as_list()
    for product in products:
        user = db(db.user.id == product["user_id"]).select().first()
        username = user.first_name + " " + user.last_name
        product.update({"product_owner": username})
    return dict(products=products)

@action('searchBar')
@action.uses()
def searchBar():
    """Gets the list of products, possibly in response to a query."""
    query = request.params.get('q')
    if query:
        no_space_query = query.strip()
        q = ((db.product.product_name.contains(no_space_query)) |
             (db.product.description.contains(no_space_query)))
    else:
        q = db.product.id > 0
    # This is a bit simplistic; normally you would return only some of
    # the products... and add pagination... this is up to you to fix.
    results = db(q).select(db.product.ALL).as_list()
    # Fixes some fields, to make it easy on the client side.
    for result in results:
        result['desired_quantity'] = min(1, result['quantity'])
        result['cart_quantity'] = 0
        user = db(db.user.id == result["user_id"]).select().first()
        username = user.first_name + " " + user.last_name
        result.update({"result_owner": username})
    return dict(
        results=results,
    )

@action('add_wishlist', method=["POST"])
@action.uses(db, auth.user, url_signer.verify())
def add_wishlist():
    product_id = request.json.get("product_id")
    product_owner = request.json.get("product_owner")
    product_Info = db(db.product.id == product_id).select().first()
    db.wishlist.update_or_insert(
        ((db.wishlist.user_id == get_user()) & (db.wishlist.product_id == product_id)),
        user_id = get_user(),
        product_id = product_id,
        product_owner = product_owner,
        product_name = product_Info.product_name,
        quantity = product_Info.quantity,
        price = product_Info.price,
        image = product_Info.image,
        description = product_Info.description,
    )
    return "ok"

#----------------------------------Layout Setting ------------------------------------
@action('registration', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'registration.html')
def registration():
    id=db(db.user.email == get_user_email()).select().first().id
    form = Form(
        [Field('nickname'),
         Field('sex'),
         Field('day', 'integer', requires=IS_INT_IN_RANGE(1, 32)),
         Field('month', requires=IS_INT_IN_RANGE(1, 13)),
         Field('year', requires=IS_INT_IN_RANGE(1800, 1e6)),
         Field('age', requires=IS_INT_IN_RANGE(0, 150)),
         Field('zipcode'),
         Field('user_description', 'text', default="Sorry, I do not write anything right now ^_^!")], 
        csrf_session=session,
        formstyle=FormStyleBulma)
    if form.accepted:
        check=db(db.user_option_Info.user_id == id).select().first()
        if check == None:
            db.user_option_Info.insert(
                user_id=id,                        ########################TODO: FOREIGN KEY constraint failed#############
                nickname=form.vars['nickname'],
                sex=form.vars['sex'],
                day=form.vars['day'],
                month=form.vars['month'],
                year=form.vars['year'],
                age=form.vars['age'],
                zipcode=form.vars['zipcode'],
                user_description=form.vars['user_description']
            )
        else: 
            db(db.user_option_Info.user_id == id).update(
                nickname=form.vars['nickname'],
                sex=form.vars['sex'],
                day=form.vars['day'],
                month=form.vars['month'],
                year=form.vars['year'],
                age=form.vars['age'],
                zipcode=form.vars['zipcode'],
                user_description=form.vars['user_description']
            )
        redirect(URL('index'))
    return dict(form=form)
#======================================================================================


#--------------------------Layout user_profile----------------------------------------
@action('user_profile')
@action.uses(db, auth.user, 'user_profile.html')
def user_profile():
    form = Form(db.user_rate_it, csrf_session=session, formstyle=FormStyleBulma)
    return dict(
        upload_user_image_url = URL('upload_user_image', signer=url_signer),
        load_Info_url = URL('load_Info', signer=url_signer),
        show_items_url = URL('show_items', signer=url_signer),
        show_community_status_url = URL('show_community_status', signer=url_signer),
        delete_post_url = URL('delete_post', signer=url_signer),
        form=form
    )

@action('show_community_status')
@action.uses(db, auth, url_signer.verify())
def show_community_status():
    id = request.params.get("user_id")
    posts = db(db.post.user_id == id).select().as_list()
    return dict(posts=posts)

@action('show_items')
@action.uses(db, auth, url_signer.verify())
def show_items():
    id = request.params.get("user_id")
    print(id)
    products = db(db.product.user_id == id).select().as_list()
    return dict(products=products) 

@action('load_Info')
@action.uses(db, auth.user, url_signer.verify())
def load_Info():
    user = db(db.user.email == get_user_email()).select().as_list()
    user_id = user[0]['id']
    user_Info = db(db.user_option_Info.user_id == user_id).select().as_list()
    if len(user_Info) > 0: 
        user[0].update(user_Info[0])
    else:
        user[0].update({'user_id':user_id, 'user_description': "Sorry, I do not write anything right now ^_^!"})
        db.user_option_Info.update_or_insert(
            (db.user_option_Info.user_id == user_id),
                user_id=user_id,
                user_description="Sorry, I do not write anything right now ^_^!"
        )
    return dict(user=user[0])


@action('upload_user_image', method= "POST")
@action.uses(db, auth.user, url_signer.verify())
def upload_user_image():
    id = db(db.user.email == get_user_email()).select().first().id
    image = request.json.get("image")
    check = db(db.user_option_Info.user_id == id).select().first()
    if check is None:
        db.user_option_Info.insert(
            user_id = id,
            user_image = image,
        )
    else:    
        db(db.user_option_Info.user_id == id).update(
            user_image = image
        )
    return "ok"
#==============================================================================


#------------------------------Layout Community part---------------------------

@action("community")
@action.uses(db, auth, url_signer, "community.html")
def community():
    return dict(
        load_community_url = URL("load_community", signer=url_signer),
        add_post_url = URL("add_post", signer=url_signer),
        delete_post_url = URL("delete_post", signer=url_signer),
        update_image_url = URL("update_image", signer=url_signer),
        set_rating_url = URL("set_rating", signer=url_signer),
        get_rating_url = URL("get_rating", signer=url_signer),
        person_number_url = URL("person_number", signer=url_signer),
    )

@action("load_community")
@action.uses(db, auth, url_signer.verify())
def load_community():
    user = db(db.user.email == get_user_email()).select().as_list()
    check = db(db.user.email == get_user_email()).select().first()
    if check is not None:
        user_id = check.id
        user_option_Info = db(db.user_option_Info.user_id == user_id).select().as_list()
        if len(user_option_Info) > 0:
            user[0].update(user_option_Info[0])
    else:
        user_id = None
    posts = db(db.post).select().as_list()
    return dict(
        user = user,
        user_id = user_id,
        posts = posts,
    )

@action("add_post", method="POST")
@action.uses(db, url_signer.verify())
def add_post():
    user = db(db.user.email == get_user_email()).select().first()
    print(user)
    check_Info = db(db.user_option_Info.user_id == user.id).select().first()
    print(check_Info)
    if check_Info is not None:
        if check_Info.nickname is not None:
            post_username = user.first_name + " " + user.last_name
        else:
            post_username = user.first_name + " " + user.last_name
        if check_Info.user_image is not None:
            post_user_image = check_Info.user_image
        else:
            post_user_image = ""
    else:
        post_username = user.first_name + " " + user.last_name
        post_user_image = ""
    post_id=db.post.insert(
        user_id = user.id,
        post_content = request.json.get("post_content"),
        post_username = post_username,
        post_user_image = post_user_image,
    )
    post = db(db.post.id == post_id).select().as_list()
    return dict(post=post)

@action("delete_post")
@action.uses(db, auth.user, url_signer.verify())
def delete_post():
    id = request.params.get('id')
    user=db(db.user.email == get_user_email()).select().first()
    username = user.first_name + " " + user.last_name
    db(
        (db.post.id == id) &
        (db.post.user_id == user.id)
    ).delete()
    return "GG"

@action("update_image", method="POST")
@action.uses(db, auth.user, url_signer.verify())
def update_image():
    id = request.json.get("id")
    image = request.json.get("image")
    db(db.post.id == id).update(
        post_user_image= image
    )
    return "ok"

@action('get_rating')
@action.uses(url_signer.verify(), db, auth.user)
def get_rating():
    """Returns the rating for a user and an image."""
    id = request.params.get('row_id')
    row = db((db.thumbs.post_id == id) &
             (db.thumbs.rater == get_user())).select().first()
    rating_up = row.rating_up if row is not None else False
    rating_down = row.rating_down if row is not None else False
    return dict(rating_up=rating_up, rating_down=rating_down)

 

@action('set_rating', method='POST')
@action.uses(auth.user, url_signer.verify(), db)
def set_rating():
    """Sets the rating for an image."""
    id = request.json.get('post_id')
    rating_up = request.json.get('rating_up')
    rating_down = request.json.get('rating_down')
    liked_user_Name = []
    disliked_user_Name = []
    assert id is not None and rating_up is not None and rating_down is not None
    db.thumbs.update_or_insert(
        ((db.thumbs.post_id == id) & (db.thumbs.rater == get_user())),
        post_id=id,
        rating_up=rating_up,
        rating_down=rating_down,
        rater=get_user(),
    )
    test= db((db.thumbs.post_id == id) & (db.thumbs.rater == get_user())).select().as_list()
    print('rating_up', rating_up)
    print('rating_down', rating_down)
    print('post_id', id)
    print('test:', test)
    post_liked_info = db(
        (db.thumbs.post_id == id) &
        (db.thumbs.rating_up == True) 
    ).select()
    for person in post_liked_info:
        liked_user = db(db.user.id == person.rater).select().first()
        liked_user_Name = liked_user_Name + [liked_user.first_name + " " + liked_user.last_name]
    post_disliked_info = db(
        (db.thumbs.post_id == id) &
        (db.thumbs.rating_down == True) 
    ).select()
    for person in post_disliked_info:
        disliked_user = db(db.user.id == person.rater).select().first()
        disliked_user_Name = disliked_user_Name + [disliked_user.first_name + " " + disliked_user.last_name]
    return dict(liked_user_Name=liked_user_Name, disliked_user_Name=disliked_user_Name)

@action("person_number")
@action.uses(db, url_signer.verify())
def person_number():
    id = request.params.get("id")
    status= request.params.get("status")
    if status == "up":
        person_rate = db(
            (db.thumbs.post_id == id) &
            (db.thumbs.rating_up == True)
        ).select().as_list()
        person_num = len(person_rate)
    elif status == "down":
        person_rate = db(
            (db.thumbs.post_id == id) &
            (db.thumbs.rating_down == True)
        ).select().as_list()
    person_num = len(person_rate)
    return dict(person_num=person_num)


#==============================================================================

#--------------------------------------Visitor------------------------------------------
@action("visitor/<user_id:int>", method=["GET", "POST"])
@action.uses(db, auth, "visitor.html")
def visitor(user_id=None):
    #TODO: 暂时没用到下一行，可删ing
    form = Form(db.user_rate_it, csrf_session=session, formstyle=FormStyleBulma)
    return dict(
        visitor_load_Info_url = URL('visitor_load_Info', user_id, signer=url_signer),
        show_items_url = URL('show_items', signer=url_signer),
        show_community_status_url = URL('show_community_status', signer=url_signer),
        delete_post_url = URL('delete_post', signer=url_signer),
        form=form,
    )

@action("visitor_load_Info/<user_id:int>", method=["GET", "POST"])
@action.uses(db, auth, url_signer.verify())
def visitor_load_Info(user_id=None):
    user = db(db.user.id == user_id).select().as_list()
    user_id = user[0]['id']
    user_Info = db(db.user_option_Info.user_id == user_id).select().as_list()
    if len(user_Info) > 0: 
        user[0].update(user_Info[0])
    else:
        user[0].update({'user_description': "Sorry, I do not write anything right now ^_^!"})
    return dict(user=user[0])
#==============================================================================




#--------------------------------------manage_products------------------------------------------
 
@action('manage_products')
@action.uses(db, auth.user, url_signer, 'manage_products.html')
def manage_products():
    return dict(
        # This is the signed URL for the callback.
        load_url = URL('load_products', signer=url_signer),
        add_url = URL('add_product', signer=url_signer),
        delete_url = URL('delete_product', signer=url_signer),
        edit_url = URL('edit_product', signer=url_signer),
        upload_url = URL('upload_image', signer=url_signer),
        add_more_url = URL('add_more', signer=url_signer),
        load_image_url = URL('load_image', signer=url_signer),
    )

# This is our very first API function.
@action('load_products')
@action.uses(auth.user, url_signer.verify(), db)
def load_products():
    id = db(db.user.email == get_user_email()).select().first().id
    rows = db(db.product.user_id == id).select().as_list()
    return dict(rows=rows)

@action('add_product', method="POST")
@action.uses(auth, url_signer.verify(), db)
def add_product():
    user_id=db(db.user.email == get_user_email()).select().first().id
    description=request.json.get('description')
    if description == "":
        description="Sorry, the owner do not add any description!"
    id = db.product.insert(
        user_id=user_id,
        product_name=request.json.get('product_name'),
        quantity=request.json.get('quantity'),
        price=request.json.get('price'),
        description=description,
    )
    return dict(id=id)

@action('delete_product')
@action.uses(auth, url_signer.verify(), db)
def delete_product():
    id = request.params.get('id')
    assert id is not None
    db(db.product.id == id).delete()
    return "ok"

@action('edit_product', method="POST")
@action.uses(auth, url_signer.verify(), db)
def edit_product():
    id = request.json.get("id")
    field = request.json.get("field")
    value = request.json.get("value")
    db(db.product.id == id).update(**{field: value})
    return "ok"

@action('upload_image', method="POST")
@action.uses(auth, url_signer.verify(), db)
def upload_image():
    product_id = request.json.get("product_id")
    image = request.json.get("image")
    db(db.product.id == product_id).update(image=image)
    return "ok"

@action('add_more', method="POST")
@action.uses(auth, url_signer.verify(), db)
def add_more():
    product_id = request.json.get("product_id")
    more_image = request.json.get("more_image")
    db.more_image.insert(
        product_id = product_id,
        more_image = more_image,
    )
    return "ok"

@action('load_image', method="GET")
@action.uses(auth, url_signer.verify(), db)
def add_more():
    product_id = request.params.get("product_id")
    more_image = db(db.more_image.product_id == product_id).select().as_list()
    return dict(more_image=more_image)
#==================================================================================

#--------------------------------------WishList------------------------------------------
@action('wishlist')
@action.uses(db, auth.user, "wishlist.html")
def wishlist():
    return dict(
        load_wishlist_url = URL('load_wishlist', signer=url_signer),
        delete_wishlist_url = URL('delete_wishlist', signer=url_signer),
        get_username_url = URL('get_username', signer=url_signer),

    )

@action('load_wishlist')
@action.uses(db, auth.user, url_signer.verify())
def load_wishlist():
    wishlist = db(db.wishlist.user_id == get_user()).select().as_list()
    return dict(wishlist=wishlist)

@action('delete_wishlist')
@action.uses(db, auth.user, url_signer.verify())
def delete_wishlist():
    id = request.params.get('id')
    db(
        (db.wishlist.id == id) &
        (db.wishlist.user_id == get_user())
    ).delete()
    return "GG"
#==================================================================================

#--------------------------------------show product------------------------------------------
@action('show_product/<product_id:int>')
@action.uses(db, auth, "show_product.html")
def show_product(product_id):
    return dict(
        load_product_detail_url = URL('load_product_detail', product_id, signer=url_signer),
        add_product_post_url = URL('add_product_post', product_id, signer=url_signer),
        delete_product_post_url = URL('delete_product_post', product_id, signer=url_signer),
    )

@action('load_product_detail/<product_id:int>')
@action.uses(db, auth, url_signer.verify())
def load_product_detail(product_id):
    user = db(db.user.email == get_user_email()).select().as_list()
    product_detail = db(db.product.id == product_id).select().as_list()
    user_id = db(db.product.id == product_id).select().first().user_id
    user = db(db.user.id == user_id).select().first()
    owner = user.first_name + " " + user.last_name
    user = db(db.user.email == get_user_email()).select().as_list()
    product_detail[0].update({'owner': owner})
    more_image = db(db.more_image.product_id == product_id).select().as_list()
    posts = db(db.product_post.product_id == product_id).select().as_list()
    return dict(
        posts=posts,
        user = user,
        product_detail = product_detail,
        more_image = more_image
        )

@action("add_product_post/<product_id:int>", method="POST")
@action.uses(db, url_signer.verify())
def add_product_post(product_id):
    user = db(db.user.email == get_user_email()).select().first()
    check_Info = db(db.user_option_Info.id == user.id).select().first()
    if check_Info is not None:
        if check_Info.nickname is not None:
            post_username = check_Info.nickname
        else:
            post_username = user.first_name + " " + user.last_name
        if check_Info.user_image is not None:
            post_user_image = check_Info.user_image
        else:
            post_user_image = ""
    else:
        post_username = user.first_name + " " + user.last_name
        post_user_image = ""
    post_id=db.product_post.insert(
        product_id = product_id,
        user_id = user.id,
        post_content = request.json.get("post_content"),
        post_username = post_username,
        post_user_image = post_user_image,
    )
    post = db(db.product_post.id == post_id).select().as_list()
    return dict(post=post)

@action("delete_product_post/<product_id:int>")
@action.uses(db, auth.user, url_signer.verify())
def delete_post(product_id):
    id = request.params.get('id')
    user=db(db.user.email == get_user_email()).select().first()
    print(id, product_id, user.id)
    db(
        (db.product_post.id == id) &
        (db.product_post.product_id == product_id) &
        (db.product_post.user_id == user.id)
    ).delete()
    return "GG"

#==================================================================================
