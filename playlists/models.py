from django.db import models
from accounts.models import User
from articles.models import Article
from tracks.models import Track

# Create your models here.
class PlayList(models.Model):
    user = models.ForeignKey(User, verbose_name="등록자", null=True, on_delete=models.CASCADE, related_name='playlist')
    track = models.ForeignKey(Track, verbose_name="곡정보", null=True, on_delete=models.CASCADE, related_name='playlist')
    order = models.IntegerField(default=0, verbose_name='플레이리스트 순서')
    create_date = models.DateTimeField(auto_created=True, auto_now=True)

    # class Meta:
    #     unique_together = (("user", "order"),)