# Generated by Django 2.0 on 2017-12-18 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0007_auto_20171218_1055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deletetrack',
            options={'ordering': ['-delete_date'], 'verbose_name_plural': '삭제된 트랙'},
        ),
        migrations.AlterField(
            model_name='deletetrack',
            name='delete_date',
            field=models.DateTimeField(auto_created=True, auto_now=True, verbose_name='삭제일'),
        ),
    ]
