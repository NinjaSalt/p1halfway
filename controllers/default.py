# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

import json

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def in_tab():
    user_owners = db().select(db.profile.user_owner)
    for row in user_owners:
        if row.user_owner == auth.user.email:
            return True
    return False

def get_id():
    user_ids = db().select(db.profile.ALL)
    for row in user_ids:
        if row.user_owner == auth.user.email:
            return row.id
    return 'None'

def get_img(game):
    imgs = db().select(db.games.ALL)
    for row in imgs:
        if row.game == game:
            return row.imglink
    return 'None'

@auth.requires_login()
def create():
    if in_tab():
        return redirect(URL('profile', args=[get_id()]))
    else:
        form = SQLFORM(db.profile).process(next=URL('index'))
        return dict(form=form)

@auth.requires_login()
def search():
    grid = SQLFORM.grid(db.profile, links = [lambda row: A('View Post',_href=URL('profile',args=[row.id]))])
    return dict(grid=grid)

@auth.requires_login()
def inbox():
    response.flash = T("Welcome to your inbox!")
    return dict(message=T('Hey'))

def profile():
    profile = db.profile(request.args(0,cast=int)) or redirect(URL('index'))
    return dict(profile=profile)

def download():
    return response.download(request, db)

@auth.requires_login()
def create_message():
    """Adds a file to the server. Requires login."""
    form = SQLFORM(db.inbox_message);
    if form.process().accepted:
        session.flash = 'Post successful.'
        redirect(URL(''))
    return dict(form = form)

def show():
    message_list = db.inbox_message(request.args(0,cast=int))
    return dict(message_list = message_list)

@auth.requires_login()
def index_comments():
    blog_post_id = 4
    blog_text = "This is my blog post"
    form = SQLFORM.factory(Field('comments', 'text'),
                           hidden=dict(blog_id=blog_post_id))
    post_url = URL('add_comment', user_signature=True)
    return dict(blog_text=blog_text, form=form,
                post_url=post_url)

@auth.requires_signature()
def add_comment():
    
    db.comments.insert(comments=comments)
    return response.json(comments)