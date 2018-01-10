from django.urls import path, include
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from rest_framework.authtoken import views as rest_framework_views
from rest_framework import routers
from rest_framework.authtoken import views

from .views import *
from . import views as local_views



app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'users', PersonViewSet)

urlpatterns = [
	path('join/', join, name='join'),
	path('auth-validation/', auth_validation, name='auth_validation'),
	path('soundcloud-login/', soundcloud_login, name='soundcloud_login'),
	path('cancel/', social_cancel),
	# path('register-email/', register_email, name='register_email'),
	path('', include(router.urls)),
	# path('test/', test),
	# path('get_auth_token/', rest_framework_views.obtain_auth_token, name='get_auth_token'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)