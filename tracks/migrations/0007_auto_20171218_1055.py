# Generated by Django 2.0 on 2017-12-18 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0006_auto_20171218_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletetrack',
            name='slug',
            field=models.CharField(max_length=100, null=True, verbose_name='slug'),
        ),
    ]
