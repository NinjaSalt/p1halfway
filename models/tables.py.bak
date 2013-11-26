def get_user():
    if auth.user:
        return auth.user.email
    else:
        return 'None'

def get_username():
    if auth.user:
        user_owners = db().select(db.profile.ALL)
        for row in user_owners:
            if row.user_owner == auth.user.email:
                return row.username
        return 'None'
    else:
        return 'None'

def post_chat(str):
    db.chat_message.insert(author=get_username(), mychat=str)
    return

db.define_table('profile',
   Field('username', unique=True),
   Field('user_owner', default=get_user(), unique=True),
   Field('mystate',requires=IS_IN_SET(['California'])),
   Field('friendcode'),
   Field('picture', 'upload'),
   Field('info', 'text'),
   Field('games', requires=IS_IN_DB(db, 'games.game', '%(game)s', multiple=True)))

db.define_table('games',
   Field('game'),
   Field('imagelink'))

db.define_table('inbox_message',
    Field('author', default = get_username(), writable=False),
    Field('title',unique = True),
    Field('description','text'),
    Field('receiver_username', requires=IS_IN_DB(db, 'profile.username', '%(username)s')))

db.define_table('chat_message',
    Field('author', default = get_username(), writable=False),
    Field('mychat'))

db.define_table('comments',
    Field('comments', 'text'),
    )

db.profile.user_owner.requires = IS_NOT_IN_DB(db, db.profile.user_owner)
db.profile.user_owner.writable = db.profile.user_owner.readable = False
