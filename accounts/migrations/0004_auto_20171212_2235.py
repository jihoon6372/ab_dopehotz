# Generated by Django 2.0 on 2017-12-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_authlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='user',
            name='clips_greeting',
            field=models.TextField(blank=True, verbose_name='구독 인사말'),
        ),
        migrations.AddField(
            model_name='user',
            name='greeting',
            field=models.TextField(blank=True, verbose_name='인사말'),
        ),
        migrations.AddField(
            model_name='user',
            name='likes_greeting',
            field=models.TextField(blank=True, verbose_name='좋아요 인사말'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.CharField(blank=True, max_length=255, verbose_name='프로필 이미지'),
        ),
        migrations.AddField(
            model_name='user',
            name='soundcloud_url',
            field=models.CharField(blank=True, max_length=255, verbose_name='사운드클라우드 URL'),
        ),
    ]
