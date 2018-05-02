from django.db import models
from tracks.models import Track
from accounts.models import User

# Create your models here.
class LogType(models.Model):
    log_name = models.CharField(max_length=255, verbose_name='이름')

    class Meta:
        verbose_name_plural = '로그 타입'

    def __str__(self):
        return self.log_name


class PlayListLog(models.Model):
    track = models.ForeignKey(Track, verbose_name="트랙", on_delete=models.CASCADE, related_name='track')
    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='플레이리스트 순서')
    log =  models.ForeignKey(LogType, on_delete=models.CASCADE, verbose_name='log_name')
    create_date = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = '플레이리스트 로그'