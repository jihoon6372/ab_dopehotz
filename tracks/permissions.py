from rest_framework import permissions
# from django.contrib.auth import is_superuser
from django.contrib.auth.decorators import login_required
 
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자에게만 쓰기를 허용하는 커스텀 권한
    """
 
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # 읽기 권한
        if request.method in permissions.SAFE_METHODS:
            # return obj.user == request.user
            return True
 
        # 이 부분이 중요한데, 매개변수로 받는 obj는 우리가 해당앱에서 다루기 위해
        # 모델링하고 직렬화한 인스턴스이므로 user 인스턴스와 동일한 타입이다.
        # 즉, 항상 request.user와 동일한 인스턴스는 아니라는 것이다.
        # obj는 object의 약자로 목적이나 대상을 의미하니.
        return obj.user == request.user
        # return True


class IsAuthenticated(permissions.BasePermission):
    """
    객체의 소유자에게만 쓰기를 허용하는 커스텀 권한
    """
 
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # 읽기 권한
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
            # return True
 
        # 이 부분이 중요한데, 매개변수로 받는 obj는 우리가 해당앱에서 다루기 위해
        # 모델링하고 직렬화한 인스턴스이므로 user 인스턴스와 동일한 타입이다.
        # 즉, 항상 request.user와 동일한 인스턴스는 아니라는 것이다.
        # obj는 object의 약자로 목적이나 대상을 의미하니.
        return obj.user == request.user
        # return True