from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from tracks.permissions import IsOwnerOrReadOnly
import datetime

from .serializers import PlayListSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes
from django.db.models import Max

from .models import PlayList
from tracks.models import Track

# Create your views here.
def test_view(request):
	return render(request, 'test.html')

class PlayListViewSet(viewsets.ModelViewSet):
	serializer_class = PlayListSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		return PlayList.objects.filter(user=self.request.user).order_by('order')

	def perform_create(self, serializer):
		track = Track.objects.select_related('user').filter(track_id=self.request.data['track']).first()
		playlist = PlayList.objects.filter(user=self.request.user)
		max_count = playlist.aggregate(Max('order'))
		if not max_count['order__max']:
			order = 1
		else:
			order = max_count['order__max']+1

		serializer.save(
			track_id=track.id,
			user=self.request.user,
			order = order,
			create_date=datetime.datetime.now()
		)