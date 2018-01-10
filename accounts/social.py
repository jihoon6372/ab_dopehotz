from urllib.request import urlopen
 
from django.core.files.base import ContentFile
# from social.utils import slugify
 
USER_FIELDS = ['email', 'name']
 
def create_user(strategy, details, user=None, *args, **kwargs):
    # print('===============================')
    # print(args)
    print('===============================')
    print(details)
    print('===============================')
    # print(kwargs)
    # print('===============================')
    if user:
        user.username = details.get('username')
        user.save()
        return {'is_new': False}
 
    fields = {'email': details.get('email'), 'username': details.get('username')}
 
    if not fields:
        return
 
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }


def update_avatar(backend, response, uid, user, *args, **kwargs):
    user.username='test'
    user.save()