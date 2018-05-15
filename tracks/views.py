from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.utils.text import slugify
from django.conf import settings

import datetime

from .permissions import IsOwnerOrReadOnly
from .serializers import TrackSerializer, TrackCommentSerializer, TrackCommentDetailSerializer
from .models import Track, TrackComment, TrackLikeLog
from accounts.models import User

import requests

# Create your views here.
class TrackViewSet(viewsets.ModelViewSet):
	lookup_field = 'track_id'
	queryset = Track.objects.prefetch_related('comment').select_related('user').filter(is_deleted=False)
	serializer_class = TrackSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	renderer_classes = (JSONRenderer, )


	def create(self, request, *args, **kwargs):
		if 'track_id' not in request.data:
			return Response({'track_id' : ['이 필드는 필수 항목입니다.']}, status=status.HTTP_400_BAD_REQUEST)

		sc_data = requests.get('http://api.soundcloud.com/tracks/'+request.data['track_id']+'?client_id='+settings.SOCIAL_AUTH_SOUNDCLOUD_KEY).json()

		# 사운드클라우드의 게시물이 존재하는지 체크
		if 'errors' in sc_data:
			return Response({'message' : '사운드클라우드의 게시물을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
		user_info = User.objects.get(email=request.user)
		user_social = user_info.social_auth.all().first()

		# 사운드클라우드 계정이 등록 안 되어있을 경우
		# if not user_social:
		# 	return Response({'message' : '사운드클라우드의 계정이 등록되어 있지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

		# 본인의 게시물인지 체크
		# if user_social.uid != sc_data['user']['id']:
		# 	return Response({'message' : '사운드클라우드의 본인 게시물만 작성 가능 합니다.'}, status=status.HTTP_400_BAD_REQUEST)
			
		self.genre = sc_data.get('genre', '')
		self.image_url = sc_data.get('artwork_url', '')
		self.download_url = sc_data.get('download_url', '')
		self.waveform_url = sc_data.get('waveform_url', '')
		self.duration = sc_data.get('duration', '')

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		slug = _get_unique_slug(self.request.POST.get('title', None))
		serializer.save(
			user=self.request.user,
			slug=slug,
			genre=self.genre,
			image_url=self.image_url,
			download_url=self.download_url,
			waveform_url=self.waveform_url,
			create_date=datetime.datetime.now()
		)


	def update(self, request, *args, **kwargs):
		post_id = request.data.get('track_id', '')
		if post_id and kwargs['track_id'] != post_id:
			return Response({'message' : 'Track ID는 변경할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)	

		sc_data = requests.get('http://api.soundcloud.com/tracks/'+str(kwargs['track_id'])+'?client_id='+settings.SOCIAL_AUTH_SOUNDCLOUD_KEY).json()

		instance = self.get_object()
		instance.duration = sc_data.get('duration', 0)
		instance.save()
		
		serializer = self.get_serializer(instance, data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)


	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.track_id = None
		instance.save()




class OnStageViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Track.objects.filter(on_stage=1)
	serializer_class = TrackSerializer
	renderer_classes = (JSONRenderer, )



class TrackCommentList(viewsets.ModelViewSet):
	serializer_class = TrackCommentSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	renderer_classes = (JSONRenderer, )

	def get_queryset(self):
		track = Track.objects.select_related('user').filter(track_id=self.kwargs['track']).first()
		return TrackComment.objects.select_related('user').select_related('parent').filter(track=track.id, parent=None)

	def perform_create(self, serializer):
		track = Track.objects.select_related('user').filter(track_id=self.kwargs['track']).first()
		serializer.save(
			track_id=track.id,
			user=self.request.user,
			create_date=datetime.datetime.now()
		)



class TrackCommentDetail(viewsets.ModelViewSet):
	serializer_class = TrackCommentDetailSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	renderer_classes = (JSONRenderer, )

	def get_queryset(self):
		return TrackComment.objects.filter(pk=self.kwargs['pk'])

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.save()



def _get_unique_slug(title):
	slug = slugify(title, allow_unicode=True)
	unique_slug = slug
	num = 1

	while Track.objects.filter(slug=unique_slug).exists():
		unique_slug = '{}-{}'.format(slug, num)
		num += 1

	return unique_slug