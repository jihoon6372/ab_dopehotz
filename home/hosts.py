from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'api', settings.ROOT_URLCONF, name='api'),
    host(r'adm', settings.ADMIN_URLCONF, name='admin'),
    host(r'auth', settings.AUTH_URLCONF, name='auth'),
)