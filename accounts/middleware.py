from .models import AuthLog
from .auth_log import account_Log
from django.utils.deprecation import MiddlewareMixin

class AuthLogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if 'is_authenticated' not in request.session:
            request.session['is_authenticated'] = False

        if '_auth_user_id' in request.session:
            if request.session['is_authenticated'] != request.session['_auth_user_id']:
                account_Log(request, request.user.id, 'success')

                request.session['is_authenticated'] = request.session['_auth_user_id']
                return None