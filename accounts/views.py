from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import ugettext_lazy as _
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import logout as auth_logout, login as auth_login
from rest_framework.decorators import list_route
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from datetime import datetime

from .serializers import PersonSerializer
from accounts.models import User, DeleteUser
from .permissions import IsOwnerOrReadOnly
from .soundcloud_auth import Soundcloud_login, get_user_token
from .email_form import UserForm
from .agree_form import AgreeForm
from .auth_log import account_Log

import uuid

# Create your views here.
class PersonViewSet(viewsets.ModelViewSet):
	queryset = User.objects.filter(is_active=True)
	serializer_class = PersonSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	renderer_classes = (JSONRenderer, )

	def create(self, request, *args, **kwargs):
		return Response({'message' : '메소드 \"POST\"는 허용되지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

	@list_route()
	def me(self, request, *args, **kwargs):
		# assumes the user is authenticated, handle this according your needs
		User = get_user_model()
		self.object = get_object_or_404(User, pk=request.user.id)
		serializer = self.get_serializer(self.object)
		return Response(serializer.data)

	def perform_destroy(self, instance):
		# 계정 비활성화
		instance.is_active = False

		# 소셜 계정 삭제
		social = SocialAccount.objects.get(user=instance.id)
		delete_user = DeleteUser()
		delete_user.user_id = instance.id
		delete_user.provider = social.provider
		delete_user.uid = social.uid
		delete_user.save()		
		social.delete()
		instance.save()


# 자바스크립트 로그인시
# @csrf_exempt
def soundcloud_login(request):
	# print("HTTP_ORIGIN : "+request.META.get('HTTP_ORIGIN'))
	# 토큰 검증 (토큰을 정상적으로 받아왔는지=>사운드클라우드 토큰)
	token = request.POST.get('oauth-token')
	if not token:
		return redirect('//dopehotz.com'+settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+'#status=error&error_type=Not+Found+oauth+token')

	# 토큰 검증 (해당 토큰이 정상적인지)
	sc_user = Soundcloud_login.get_soundcloud_user(token)
	if not sc_user:
		return redirect('//dopehotz.com'+settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+'#status=error&error_type=Not+Found+user')

	user = Soundcloud_login.get_or_create_user(sc_user)

	if user.is_active:
		# # 블락 여부 체크
		# if user.is_block:
		# 	account_Log(request, user.id, 'inactive')
		# 	return redirect('//dopehotz.com'+settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+'#status=error&error_type=Account+inactive+or+deleted.')

		# 유저 검증 성공
		account_Log(request, user.id, 'success')

		# 토큰 재생성
		instance = User.objects.get(pk=user.id)
		Token.objects.get(user=user.id).delete()
		Token.objects.create(user=instance)

		msg = settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+"#status=success&access_token="+get_user_token(user.id)
		return redirect('//dopehotz.com'+msg)
	else:
		# 유저 비활성화
		if user.email.endswith('dopehotz.com'):
			# 이메일 등록 전 상태
			account_Log(request, user.id, 'success')
			request.session['user'] = user.id
			return redirect('accounts:register_email')
		else:
			# 블락된 계정
			account_Log(request, user.id, 'blocked')
			return redirect('//dopehotz.com'+settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+'#status=error&error_type=Account+is+blocked.')


def register_email(request):
	user = request.session.get('user', None)
	if not user:
		raise Http404

	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user = User.objects.get(pk=user)
			if not user.is_active:
				user.email = request.POST.get('email')
				user.is_active = True
				user.save()
				del request.session['user']
				return redirect('//dopehotz.com/#status=success&access_token='+get_user_token(user.id))

	else:
		form = UserForm()

	return render(request, 'accounts/email_form.html', {'form': form,})




# 서버 로그인시

def join(request):
	current_user = request.session.get('current_user', None)
	socialaccount_sociallogin = request.session.get('socialaccount_sociallogin', None)
	if not current_user and not socialaccount_sociallogin:
		raise Http404

	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			password = '!'+str(uuid.uuid4()).replace("-", "")

			# 유저 생성
			user = User.objects.create(email=request.POST.get('email'), password=password)
			mailing_agree = request.POST.get('mailing_agree', None)

			# 소셜 정보 생성
			social_auth = SocialAccount()
			if current_user:
				social_user = request.session['current_user']['obj']
				social_auth.provider = 'soundcloud'
				social_auth.uid = social_user['id']
				user.username = social_user['username']
				user.soundcloud_url = social_user['permalink_url']
				user.profile_picture = social_user['avatar_url']
				social_auth.user_id = user.id

			if socialaccount_sociallogin:
				social_user = request.session['socialaccount_sociallogin']['account']
				social_auth.provider = social_user['provider']
				social_auth.uid = social_user['uid']
				social_auth.user_id = user.id
				if 'naver' in social_user['provider']:
					user.username = social_user['extra_data'].get('name', social_user['extra_data']['nickname'])
					user.profile_picture = social_user['extra_data'].get('profile_image', '')
				else:
					user.username = social_user['extra_data'].get('name', '')
			
			social_auth.save()
			
			if mailing_agree and 'on' in mailing_agree:
				user.mailing_agree = True
			user.last_login = datetime.now()
			user.save()

			auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			


			# 콜백
			# msg = settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+"#status=success&access_token="+get_user_token(user.id)
			return auth_redirect(request, "#status=success&access_token="+get_user_token(user.id))
			# return redirect('//dopehotz.com'+msg)

	else:
		form = UserForm()
	
	return render(request, 'accounts/join_form.html', {'form': form, 'main_site' : settings.MAIN_URL})



def auth_validation(request):
	uid = None

	if 'current_user' in request.session:
		uid = request.session['current_user']['obj']['id']

	if 'uid' in request.session:
		uid = request.session['uid']

	if not uid:
		raise Http404

		

	# 기존 회원인지 체크
	try:
		social_auth = SocialAccount.objects.get(uid=uid)

		user = User.objects.get(pk=social_auth.user_id)
		user.last_login = datetime.now()
		user.save()
		

		if user.is_active:
			# 유저 검증 성공
			account_Log(request, user.id, 'success')

			# 토큰 재생성
			instance = User.objects.get(pk=user.id)
			Token.objects.get(user=user.id).delete()
			Token.objects.create(user=instance)

			msg = settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+"#status=success&access_token="+get_user_token(user.id)
			return auth_redirect(request, "#status=success&access_token="+get_user_token(user.id))
			# return redirect('//dopehotz.com'+msg)
		else:
			# 블락된 계정
			account_Log(request, user.id, 'blocked')
			return auth_redirect(request, '#status=error&error_type=Account+is+blocked+or+deleted.')
			# return redirect('//dopehotz.com'+settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+'#status=error&error_type=Account+is+blocked.')


	except SocialAccount.DoesNotExist:
		return redirect('accounts:join')

	return render(request, 'callback.html')


def auth_redirect(request, msg):
	current_user = request.session.get('current_user', None)
	socialaccount_sociallogin = request.session.get('socialaccount_sociallogin', None)
	uid = request.session.get('uid', None)

	if not current_user and not socialaccount_sociallogin and not uid:
		raise Http404

	if current_user:
		del request.session['current_user']
	if socialaccount_sociallogin:
		del request.session['socialaccount_sociallogin']
	if uid:
		del request.session['uid']

	# if 'is_authenticated' in  request.session:
		# auth_logout(request)


	return redirect('//dopehotz.com'+settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL+msg)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def social_cancel(request, **kwargs):
	return HttpResponse('test')
	

def test(request):
	# print('aaa2')
	print(request.META)
	return HttpResponse('test')