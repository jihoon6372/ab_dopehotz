from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
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
from logs.models import PlayListLog

# Create your views here.
def test_view(request):
	return render(request, 'test.html')

class PlayListViewSet(viewsets.ModelViewSet):
	serializer_class = PlayListSerializer
	permission_classes = (permissions.IsAuthenticated,)
	renderer_classes = (JSONRenderer, )

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

		# 로그 기록
		log = PlayListLog()
		log.track_id=track.id
		log.user=self.request.user
		log.order = order
		log.log_id = 1
		log.save()

	
	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		# 로그 기록
		log = PlayListLog()
		log.track_id = instance.track_id
		log.user = self.request.user
		log.order = serializer.data['order']
		log.log_id = 2
		log.save()
		return Response(serializer.data)


	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()

		# 로그 기록
		log = PlayListLog()
		log.track_id = instance.track_id
		log.user = self.request.user
		log.order = instance.order
		log.log_id = 3
		log.save()

		self.perform_destroy(instance)
		return Response(status=status.HTTP_204_NO_CONTENT)