from django.db import models
from accounts.models import User
from django.utils.text import slugify

# Create your models here.

class TrackManager(models.Manager):
	def all(self):
		qs = super(TrackManager, self).select_related('user').all()
		return qs

class Track(models.Model):
	# id = models.IntegerField(primary_key=True, editable=True)
	track_id = models.IntegerField(null=True, unique=True, verbose_name='트랙 ID')
	title = models.CharField('제목', max_length=100)
	slug = models.SlugField('SLUG', unique=True, max_length=100, allow_unicode=True, null=True, help_text='자동 입력')
	user = models.ForeignKey(User, verbose_name="작성자", null=True, on_delete=models.CASCADE, related_name='tracks')
	tape_info = models.TextField(blank=True, null=True, verbose_name='Tape INFO')
	lyrics = models.TextField(blank=True, null=True, verbose_name='lyrics')
	hashtag = models.TextField(blank=True, null=True, verbose_name='해시태그')
	genre = models.CharField(max_length=255, blank=True, null=True, verbose_name='장르')
	image_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='이미지 URL')
	download_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='다운로드 URL')
	waveform_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='Waveform URL')
	comments = models.IntegerField(default=0, verbose_name='댓글 수')
	view_count = models.IntegerField(default=0, verbose_name='조회 수')
	likes = models.IntegerField(default=0, verbose_name='좋아요')
	clips = models.IntegerField(default=0, verbose_name='구독')
	track_score = models.IntegerField(default=0, verbose_name='트랙 점수')
	on_stage = models.IntegerField(default=0, db_index=True, verbose_name='온스테이지')
	is_deleted = models.BooleanField(default=False, verbose_name='삭제여부', help_text='트랙을 삭제하는 대신 이부분을 체크 하세요.')
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)
	duration = models.IntegerField(default=0, verbose_name='곡 길이')

	objects = TrackManager()

	class Meta:
		verbose_name_plural = '트랙'
		ordering = ['-create_date']

	def __str__(self):
		return self.title

	def _get_unique_slug(self):
		slug = slugify(self.title, allow_unicode=True)
		unique_slug = slug
		num = 1

		while Track.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1

		return unique_slug

	@property
	def comment(self):
		instance = self
		qs = TrackComment.objects.filter_by_instance(instance)
		return qa


	def save(self, *args, **kargs):
		if not self.id:
			self.slug = self._get_unique_slug()
			
		super(Track, self).save(*args, **kargs)


# class DeleteTrack(models.Model):
# 	track_id = models.IntegerField(blank=True, null=True)
# 	title = models.CharField('제목', max_length=100)
# 	slug = models.CharField('slug', max_length=100, null=True)
# 	user = models.ForeignKey(User, verbose_name="작성자", null=True, on_delete=models.CASCADE, related_name='delete_tracks')
# 	tape_info = models.TextField(blank=True, null=True, verbose_name='Tape INFO')
# 	lyrics = models.TextField(blank=True, null=True, verbose_name='lyrics')
# 	hashtag = models.CharField(max_length=255, blank=True, null=True, verbose_name='해시태그')
# 	genre = models.CharField(max_length=255, blank=True, null=True, verbose_name='장르')
# 	image_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='이미지 URL')
# 	download_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='다운로드 URL')
# 	waveform_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='Waveform URL')
# 	comments = models.IntegerField(default=0, verbose_name='댓글 수')
# 	view_count = models.IntegerField(default=0, verbose_name='조회 수')
# 	likes = models.IntegerField(default=0, verbose_name='좋아요')
# 	clips = models.IntegerField(default=0, verbose_name='구독')
# 	track_score = models.IntegerField(default=0, verbose_name='트랙 점수')
# 	on_stage = models.IntegerField(default=0, verbose_name='온스테이지')
# 	create_date = models.DateTimeField(auto_created=True, auto_now=True)
# 	update_date = models.DateTimeField(auto_now=True)
# 	delete_date = models.DateTimeField(auto_created=True, auto_now=True, verbose_name='삭제일')

# 	class Meta:
# 		verbose_name_plural = '삭제된 트랙'
# 		ordering = ['-delete_date']

# 	def __str__(self):
# 		return self.title

class TrackCommentManager(models.Manager):
	def all(self):
		qs = super(TrackCommentManager, self).select_related('user').select_related('parent').filter(is_deleted=False)
		return qs

	def filter_by_instance(self, instance):
		qs = super(TrackCommentManager, self).select_related('user').select_related('parent').filter(pk=instance.id, parent=None, is_deleted=False)
		return qs


class TrackComment(models.Model):
	track = models.ForeignKey(Track, verbose_name="트랙", on_delete=models.CASCADE, related_name='comment')
	parent = models.ForeignKey("self", verbose_name="부모 댓글", on_delete=models.CASCADE, null=True, blank=True, related_name='children')
	user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
	contents = models.TextField(verbose_name='댓글')
	is_deleted = models.BooleanField(default=False, verbose_name='삭제여부', help_text='댓글을 삭제하는 대신 이부분을 체크 하세요.')
	create_date = models.DateTimeField(auto_created=True)
	update_date = models.DateTimeField(auto_now=True)

	objects = TrackCommentManager()

	class Meta:
		verbose_name_plural = '댓글'
		ordering = ['-create_date']
			

	def __str__(self):
		return self.contents


class TrackLikeType(models.Model):
	like_type = models.CharField(max_length=255, verbose_name='좋아요 타입')

	class Meta:
		verbose_name_plural = '트랙 좋아요 타입'

	def __str__(self):
		return self.like_type


class TrackLikeLog(models.Model):
	track_like_type = models.ForeignKey(TrackLikeType, verbose_name="좋아요 타입", on_delete=models.CASCADE)
	track = models.ForeignKey(Track, blank=True, null=True, verbose_name="트랙", on_delete=models.CASCADE, related_name='TrackLog')
	user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
	create_date = models.DateTimeField(auto_created=True)

	class Meta:
		verbose_name_plural = '트랙 좋아요 로그'
		ordering = ['-create_date']
