from django.urls import path, include
from django.conf import settings
from .views import *
from rest_framework import routers


app_name = 'tracks'

# router = routers.DefaultRouter()
# router.register(r'', TrackViewSet)
# router.register(r'', TrackCommentViewSet)

urlpatterns = [
	path('', TrackViewSet.as_view({'get':'list', 'post':'create'})),
	path('<int:track_id>/', TrackViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('on-stage/', OnStageViewSet.as_view({'get':'list'})),
    path('on-stage/<int:pk>/', OnStageViewSet.as_view({'get':'retrieve'})),
    path('<int:track>/comments/', TrackCommentList.as_view({'get':'list', 'post':'create'})),
    path('<int:track>/comments/<int:pk>/', TrackCommentDetail.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    # path('', include(router.urls)),
]