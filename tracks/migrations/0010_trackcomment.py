# Generated by Django 2.0 on 2017-12-18 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracks', '0009_auto_20171218_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_created=True, auto_now=True)),
                ('contents', models.TextField(verbose_name='댓글')),
                ('is_delete', models.BooleanField(default=False, verbose_name='삭제여부')),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracks.TrackComment')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='tracks.Track', verbose_name='트랙')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'verbose_name_plural': '댓글',
                'ordering': ['-create_date'],
            },
        ),
    ]
