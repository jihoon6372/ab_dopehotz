# Generated by Django 2.0 on 2017-12-18 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0014_auto_20171218_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_sub', to='tracks.TrackComment', verbose_name='부모 댓글'),
        ),
    ]
