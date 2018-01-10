from rest_framework import serializers

from accounts.models import User


class MeSerializer(serializers.ModelSerializer):
	
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
		)
		read_only_fields = ('email', 'username','soundcloud_url', 'profile_picture')

