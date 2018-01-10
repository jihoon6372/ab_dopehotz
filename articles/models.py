from django.db import models
from accounts.models import User

# Create your models here.
class Article(models.Model):
	title = models.CharField('제목', max_length=100)
	slug = models.SlugField('SLUG', unique=True, max_length=100, allow_unicode=True, null=True, help_text='자동 입력')
	user = models.ForeignKey(User, verbose_name="작성자", null=True, on_delete=models.CASCADE, related_name='articles')
	content = models.TextField('내용')
	is_deleted = models.BooleanField('삭제여부', default=False, help_text='사용자가 게시물을 삭제 했을 경우')
	create_date = models.DateTimeField(auto_created=True, auto_now=True)
	update_date = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = '자유게시판'


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

	def save(self, *args, **kargs):
		if not self.id:
			self.slug = self._get_unique_slug()
			
		super(Track, self).save(*args, **kargs)