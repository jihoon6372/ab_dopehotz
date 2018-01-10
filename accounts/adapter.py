from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url
from datetime import datetime, timedelta

class AccountAdapter(DefaultAccountAdapter):

	def get_login_redirect_url(self, request):
		print('self===============')
		print(self.__dict__)
		print('request============')
		print(request.__dict__)

		request.user.username = 'test'
		request.user.save()

		url = settings.LOGIN_REDIRECT_URL
		return resolve_url(url)
		# assert request.user.is_authenticated()
		# if (request.user.last_login - request.user.date_joined).seconds < threshold:
		#     url = '/registration/success'
		# else:
		#     url = settings.LOGIN_REDIRECT_URL
		# return resolve_url(url)