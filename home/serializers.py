from rest_framework import serializers
from django.utils import timezone
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


class DateTimeFieldWihTZ(serializers.DateTimeField):
    '''Class to make output of a DateTime Field timezone aware
    '''
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)