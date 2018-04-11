from accounts.models import User
from tracks.models import Track, TrackComment
from .models import PlayList
from rest_framework import serializers
from social_django.models import UserSocialAuth
from rest_framework.validators import UniqueTogetherValidator

from tracks.serializers import TrackSerializer
# from rest_framework.decorators import detail_route

class PersonSerializer(serializers.ModelSerializer):
	# social_auth = SocialSerializer(many=True, read_only=True)
	class Meta:
		model = User
		fields = (
			'email',
			'username',
			'soundcloud_url',
			'profile_picture',
		)

class PlayListSerializer(serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = PlayList
        fields = (
			'id',
            'track',
            'order'
        )