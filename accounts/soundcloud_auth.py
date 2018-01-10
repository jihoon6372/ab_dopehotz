#third party
from social_django.models import UserSocialAuth
from rest_framework.authtoken.models import Token

#custom app
from accounts.models import User

#system
import requests
import json
import uuid
from datetime import datetime

class Soundcloud_login(object):

	def get_soundcloud_user(token):
		link = 'https://api.soundcloud.com/me?oauth_token='+token
		data = requests.get(link)

		if data.status_code == requests.codes.ok:
			data = data.json()
			return data


	def get_or_create_user(soundcloud_user):
		try:
			social_auth = UserSocialAuth.objects.get(uid=soundcloud_user['id'])
			user = User.objects.get(pk=social_auth.user_id)
			user.last_login = datetime.now()
			user.save()
			return user
		except UserSocialAuth.DoesNotExist:
			useremail = str(uuid.uuid4()).replace("-", "")+'@dopehotz.com'
			password = '!'+str(uuid.uuid4()).replace("-", "")

			while User.objects.filter(email=useremail).exists():
				useremail = str(uuid.uuid4()).replace("-", "")+'@dopehotz.com'

			user = User.objects.create(email=useremail, password=password)

			social_auth = UserSocialAuth()
			social_auth.provider = 'soundcloud'
			social_auth.uid = soundcloud_user['id']
			social_auth.user_id = user.id
			social_auth.save()

			user.is_active = 0
			user.username = soundcloud_user['username']
			user.soundcloud_url = soundcloud_user['permalink_url']
			user.profile_picture = soundcloud_user['avatar_url']
			user.last_login = datetime.now()
			user.save()

			return user


		

def get_user_token(userid):
	token = Token.objects.get(user=userid)
	return token.key