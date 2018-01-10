from .models import AuthLog

def account_Log(request, userid, type):
	a = AuthLog()
	a.user_id = userid
	a.ip_address = request.META.get('REMOTE_ADDR', '')
	a.user_agent = request.META.get('HTTP_USER_AGENT', '')
	a.state = type
	a.save()