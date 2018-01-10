from rest_framework import permissions
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
            return True
 
        # 쓰기 권한
        return obj == request.user