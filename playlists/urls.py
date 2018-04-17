from django.urls import path, include
from django.conf import settings
from .views import *


app_name = 'playlist'
# router = routers.DefaultRouter()
# router.register(r'', TrackViewSet)
# router.register(r'', TrackCommentViewSet)

urlpatterns = [
    # path('', test_view),
    path('', PlayListViewSet.as_view({'get':'list', 'post':'create'})),
    path('<int:pk>/', PlayListViewSet.as_view({'put':'update', 'delete':'destroy'})),
	# path('', TrackViewSet.as_view({'get':'list', 'post':'create'})),
	# path('<int:track_id>/', TrackViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    # path('on-stage/', OnStageViewSet.as_view({'get':'list'})),
    # path('on-stage/<int:pk>/', OnStageViewSet.as_view({'get':'retrieve'})),
    # path('<int:track>/comments/', TrackCommentList.as_view({'get':'list', 'post':'create'})),
    # path('<int:track>/comments/<int:pk>/', TrackCommentDetail.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    # path('', include(router.urls)),
]