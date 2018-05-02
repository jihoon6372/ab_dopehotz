from accounts.models import User
from tracks.models import Track, TrackComment
from rest_framework import serializers
from social_django.models import UserSocialAuth
from rest_framework.validators import UniqueTogetherValidator
from home.serializers import DateTimeFieldWihTZ
# from rest_framework.decorators import detail_route

class SocialSerializer(serializers.ModelSerializer):
	# queryset = UserSocialAuth.objects.select_related('user').all()
	class Meta:
		model = UserSocialAuth
		fields = ('provider', 'uid')

	def get_queryset(self):
		assert self.queryset is not None, (
		    "'%s' should either include a `queryset` attribute, "
		    "or override the `get_queryset()` method."
		    % self.__class__.__name__
		)

		queryset = self.queryset
		if isinstance(queryset, QuerySet):
			# Ensure queryset is re-evaluated on each request.
			queryset = queryset.select_related('user').all()
		return queryset

class PersonSerializer(serializers.ModelSerializer):
	# social_auth = SocialSerializer(many=True, read_only=True)
	class Meta:
		model = User
		fields = (
			'id',
			'email',
			'username',
			'soundcloud_url',
			'profile_picture',
			# 'social_auth'
		)

class SubTrackCommentSerializer(serializers.ModelSerializer):
	user = PersonSerializer(read_only=True)
	#create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
	# replies = serializers.SerializerMethodField()
	create_date = DateTimeFieldWihTZ(format='%Y-%m-%d %H:%M:%S')

	class Meta:
		model = TrackComment
		fields = (
			'id',
			'contents',
			'track_id',
			'parent',
			'user',
			'create_date',
			# 'replies',
		)

	

	# def get_replies(self, obj):
	# 	if obj.children:
	# 		return SubTrackCommentSerializer(obj.children, many=True).data
	# 	return None

class TrackCommentSerializer(serializers.ModelSerializer):
	user = PersonSerializer(read_only=True)
	# reply_count = serializers.SerializerMethodField()
	replies = serializers.SerializerMethodField(read_only=True)
	create_date = DateTimeFieldWihTZ(format='%Y-%m-%d %H:%M:%S')

	class Meta:
		model = TrackComment
		fields = (
			'id',
			'contents',
			'track_id',
			'parent',
			'user',
			# 'reply_count',
			'create_date',
			'replies'
		)

		read_only_fields = ('create_date',)

	# def get_reply_count(self, obj):
	# 	if obj.children:
	# 		return obj.children.count()
	# 	return 0

	def get_replies(self, obj):
		if obj.children:
			return SubTrackCommentSerializer(obj.children, many=True).data
		return None


class TrackCommentDetailSerializer(serializers.ModelSerializer):
	user = PersonSerializer(read_only=True)
	create_date = DateTimeFieldWihTZ(format='%Y-%m-%d %H:%M:%S')

	class Meta:
		model = TrackComment
		fields = (
			'id',
			'contents',
			'parent',
			'user',
			'create_date'
		)

		read_only_fields = ('parent',)
	

class TrackSerializer(serializers.ModelSerializer):
	user = PersonSerializer(read_only=True)
	create_date = DateTimeFieldWihTZ(format='%Y-%m-%d %H:%M:%S')
	
	def get_comment_count(self, obj):
		return obj.comment.count()

	def get_comment(self, obj):
		c_qs = TrackComment.objects.filter_by_instance(obj)
		comments = TrackCommentSerializer(c_qs, many=True).data
		return comments

	comment_count = serializers.SerializerMethodField()
	comment = serializers.SerializerMethodField()

	class Meta:
		model = Track
		fields = (
			'track_id',
			'user',
			'title',
			'slug',
			'tape_info',
			'duration',
			'lyrics',
			'hashtag',
			'genre',
			'image_url',
			'download_url',
			'waveform_url',
			'view_count',
			'likes',
			'clips',
			'track_score',
			'on_stage',
			'comment_count',
			'comment',
			'create_date',
		)
		read_only_fields = (
			'user',
			'slug',
			'view_count',
			'likes',
			'clips',
			'track_score',
			'on_stage',
			'create_date',
			'genre',
			'image_url',
			'download_url',
			'waveform_url',
			'test_date_time'
		)