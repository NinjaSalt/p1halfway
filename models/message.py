# obtain user login information
def get_login():
    if auth.user:
        return auth.user.first_name + " " + auth.user.last_name
    else:
        return "Unknown User"

# obtain user id
def get_id():
    if auth.user:
        return auth.user.id
    else:
        return 0

# obtain user e-mail
def get_email():
    if auth.user:
        return auth.user.email
    else:
        return "Unknown User"


#define message layout


    # The following three fields could be useful later for accepting a person's Friend Code request an
    #Field('accepted','boolean'),
    #Field('complete','boolean'),
    #Field('rejected', 'boolean'),
