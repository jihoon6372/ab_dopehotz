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


# class TrackSerializer(serializers.ModelSerializer):
# 	user = PersonSerializer(read_only=True)
	
# 	def get_comment_count(self, obj):
# 		return obj.comment.count()

# 	# def get_comment(self, obj):
# 	# 	c_qs = TrackComment.objects.filter_by_instance(obj)
# 	# 	comments = TrackCommentSerializer(c_qs, many=True).data
# 	# 	return comments

# 	# comment = serializers.SerializerMethodField()
# 	comment_count = serializers.SerializerMethodField()
# 	# test_duration = 1000

# 	class Meta:
# 		model = Track
# 		fields = (
# 			'track_id',
# 			'user',
# 			'title',
# 			'slug',
# 			'tape_info',
# 			'duration',
# 			# 'test_duration',
# 			'lyrics',
# 			'hashtag',
# 			'genre',
# 			'image_url',
# 			'download_url',
# 			'waveform_url',
# 			'view_count',
# 			'likes',
# 			'clips',
# 			'track_score',
# 			'on_stage',
# 			'comment_count',
# 			# 'comment',
# 			'create_date'
# 		)
# 		read_only_fields = (
# 			'user',
# 			'slug',
# 			'view_count',
# 			'likes',
# 			'clips',
# 			'track_score',
# 			'on_stage',
# 			'create_date',
# 			'genre',
# 			'image_url',
# 			'download_url',
# 			'waveform_url'
# 		)

class PlayListSerializer(serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = PlayList
        fields = (
            'track',
            'order'
        )