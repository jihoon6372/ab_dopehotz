from .models import User
from tracks.models import Track
from rest_framework import serializers
from social_django.models import UserSocialAuth

class TrackSerializer(serializers.ModelSerializer):
	class Meta:
		model = Track
		fields = ('title', 'tape_info', 'track_id', 'image_url')


class SocialSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserSocialAuth
		fields = ('provider', 'uid')
		

class PersonSerializer(serializers.ModelSerializer):
	tracks = TrackSerializer(many=True, read_only=True)
	social_auth = SocialSerializer(many=True, read_only=True)

	class Meta:
		model = User
		fields = (
			'id',
			'email',
			'username',
			'soundcloud_url',
			'profile_picture',
			'greeting',
			'clips_greeting',
			'likes_greeting',
			'tracks',
			'social_auth'
		)
		read_only_fields = ('email', 'username','soundcloud_url', 'profile_picture')