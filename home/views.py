from django.shortcuts import render, redirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.views.generic import FormView, RedirectView
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth
from django.conf import settings
from django.contrib import messages
# from rest_framework import viewsets
# from rest_framework import permissions


from tracks.permissions import IsOwnerOrReadOnly
from accounts.models import User
from accounts.views import auth_redirect
from rest_framework.authtoken.models import Token
# from .serializers import MeSerializer

# from rest_framework import status
# from rest_framework.response import Response

import requests
import json
import soundcloud

def test_view(request):
	return render(request, 'test.html')


def auth_view(request):
	return render(request, 'home.html', {'main_site' : settings.MAIN_URL})


class LogoutView(RedirectView):
	url = '//dopehotz.com'

	def get(self, request, *args, **kwargs):
		auth_logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)


def sc_view(request):
	# request.session['test'] = 'asss'
	return render(request, 'sc.html')

@csrf_exempt
def test_ajax(request):
	if not request.POST.get('oauth-token'):
		return redirect('//dopehotz.com'+settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+'#status=error&error_type=Not+Found+oauth+token')

	email = request.POST.get('email')
	if not email:
		return redirect('//dopehotz.com'+settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+'#status=error&error_type=Please+enter+your+e-mail')

	link = 'https://api.soundcloud.com/me?oauth_token='+request.POST.get('oauth-token')
	data = requests.get(link)
	if data.status_code != requests.codes.ok:
		return redirect('//dopehotz.com'+settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+'#status=error&error_type=Not+Found+user')

	data = data.json()
	user, created = User.objects.get_or_create(email=email)

	if created:
		user.username = data['username']
		user.soundcloud_url = data['permalink_url']
		user.profile_picture = data['avatar_url']
		user.save()

		social_auth = UserSocialAuth()
		social_auth.provider = 'soundcloud'
		social_auth.uid = data['id']
		social_auth.user_id = user.id
		social_auth.save()

		msg = settings.SOCIAL_AUTH_NEW_USER_REDIRECT_URL+"status=success&create=true&access_token="+get_user_token(user.id)
	else:
		if user.is_active:
			msg = settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+"#status=success&create=false&access_token="+get_user_token(user.id)
		else:
			msg = settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+"status=error&create=false&error_type=account+is+not+active"

	return redirect('//dopehotz.com'+msg)


def get_user_token(userid):
	token = Token.objects.get(user=userid)
	return token.key



def callback_comp(request):
	return render(request, 'auth_comp.html')

def test(request):
	return render(request, 'test.html')



def soundcloud_login(request):
	import soundcloud
	client = soundcloud.Client(client_id=settings.SOCIAL_AUTH_SOUNDCLOUD_KEY,
                           client_secret=settings.SOCIAL_AUTH_SOUNDCLOUD_SECRET,
                           redirect_uri='https://auth.dopehotz.com/callback/')
	return redirect(client.authorize_url())


def callback(request):
	if 'error' in request.GET:
		messages.add_message(request, messages.ERROR, '로그인이 취소 되었습니다.')
		return redirect('index')

	backend = request.session.get('social_auth_last_login_backend', None)

	if backend:
		# msg = settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+"#status=success&access_token="+get_user_token(request.session['_auth_user_id'])
		auth_logout(request)
		return auth_redirect(request, '#status=success&access_token='+get_user_token(request.session['_auth_user_id']))
	
		# return redirect('//dopehotz.com'+msg)
	

	code = request.GET.get('code', None)
	if code:
		client = soundcloud.Client(client_id=settings.SOCIAL_AUTH_SOUNDCLOUD_KEY,
                           client_secret=settings.SOCIAL_AUTH_SOUNDCLOUD_SECRET,
                           redirect_uri='https://auth.dopehotz.com/callback/')
		access_token = client.exchange_token(code)

		client = soundcloud.Client(access_token=access_token.obj['access_token'])
		current_user = client.get('/me')
		request.session['current_user'] = current_user.__dict__

	return redirect('accounts:auth_validation')


def session_check(request):
	if request.user.is_authenticated:
		return HttpResponse("{'session': True, 'uid': "+request.session['_auth_user_id']+"}")
	else:
		# result = 
		return HttpResponse("{'session': False}")


def player(request):
	return render(request, 'player.html')




	